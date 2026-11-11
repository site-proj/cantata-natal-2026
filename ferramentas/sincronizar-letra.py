"""Sincroniza a letra com o áudio (karaokê): reconhecimento de voz com tempo por palavra (Whisper)
+ alinhamento da letra conhecida, linha a linha, em ordem. Gera letras/<id>.tempos.json.

Uso: python sincronizar.py <audio.mp3> <letra.txt> <saida.tempos.json> [modelo]
"""
import json, re, sys, unicodedata, difflib, time

AUDIO, LETRA, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
MODELO = sys.argv[4] if len(sys.argv) > 4 else 'small'


def norm(p):
    p = unicodedata.normalize('NFD', p.lower())
    p = ''.join(c for c in p if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', p)


ACORDE = re.compile(r'^[(\[|]*[A-G](#|b)?(m|M|maj|min|dim|aug|sus|add|º|°|\+)?\d*(\(?[#b+-]?\d+\)?)*(/[A-G](#|b)?)?[)\]|]*$')


def so_acordes(l):
    """Igual ao player: linha só de acordes (ou 'Cifras:') não entra na letra."""
    if re.match(r'^\s*cifras?:', l, re.I):
        return True
    toks = [t for t in re.sub(r'\([^)]*\)', ' ', l).split() if not re.match(r'^(\d+x|x\d+|-+|\|+|\.+)$', t, re.I)]
    return bool(toks) and sum(1 for t in toks if ACORDE.match(t)) / len(toks) >= .7


def linhas_da_letra(texto):
    """Mesmas linhas que o player mostra (sem cabeçalho de título/artista e sem 'Composição')."""
    ls = texto.replace('\r', '').rstrip().split('\n')
    ini = 0
    while ini < len(ls) and ini < 4 and ls[ini].strip():
        ini += 1
    corpo = '\n'.join(ls[ini:]).lstrip('\n')
    out = []
    for est in re.split(r'\n\s*\n', corpo):
        if re.match(r'^\s*composi[cç][aã]o', est.strip(), re.I):
            continue
        out += [l.strip() for l in est.strip().split('\n') if l.strip() and not so_acordes(l)]
    return out


def transcrever():
    from faster_whisper import WhisperModel
    t0 = time.time()
    modelo = WhisperModel(MODELO, device='cpu', compute_type='int8', cpu_threads=4)
    import subprocess, numpy as np
    bruto = subprocess.run(['ffmpeg', '-v', 'error', '-i', AUDIO, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
    onda = np.frombuffer(bruto, np.int16).astype(np.float32) / 32768.0
    segs, info = modelo.transcribe(onda, language='pt', word_timestamps=True, vad_filter=False,
                                   vad_parameters={'min_silence_duration_ms': 600}, beam_size=5, condition_on_previous_text=False)
    palavras = []
    for s in segs:
        for w in (s.words or []):
            n = norm(w.word)
            if n:
                palavras.append((n, round(w.start, 2), round(w.end, 2), w.word.strip()))
    print(f'transcrição: {len(palavras)} palavras em {time.time() - t0:.0f}s', file=sys.stderr)
    return palavras


def alinhar(linhas, palavras):
    """Alinhamento global (estilo Needleman-Wunsch) entre as palavras da letra e as reconhecidas."""
    letra = []                                   # (palavra normalizada, índice da linha)
    for i, l in enumerate(linhas):
        for p in l.split():
            n = norm(p)
            if n:
                letra.append((n, i))
    A, B = len(letra), len(palavras)
    sim = lambda a, b: 1.0 if a == b else difflib.SequenceMatcher(None, a, b).ratio()
    GAP_L, GAP_R = -0.4, -0.25                    # pular palavra da letra / pular palavra reconhecida
    NEG = -1e9
    S = [[0.0] * (B + 1) for _ in range(A + 1)]
    T = [[0] * (B + 1) for _ in range(A + 1)]     # 0 diag, 1 cima (pula letra), 2 esquerda (pula reconhecida)
    for i in range(1, A + 1):
        S[i][0] = S[i - 1][0] + GAP_L; T[i][0] = 1
    for j in range(1, B + 1):
        S[0][j] = 0.0; T[0][j] = 2                # começo livre (introdução instrumental / falas)
    for i in range(1, A + 1):
        a = letra[i - 1][0]
        for j in range(1, B + 1):
            s = sim(a, palavras[j - 1][0])
            d = S[i - 1][j - 1] + (2.0 * s - 0.8 if s >= .6 else -1.2)
            u = S[i - 1][j] + GAP_L
            e = S[i][j - 1] + GAP_R
            if d >= u and d >= e: S[i][j], T[i][j] = d, 0
            elif u >= e: S[i][j], T[i][j] = u, 1
            else: S[i][j], T[i][j] = e, 2
    # fim livre: melhor j na última linha
    j = max(range(B + 1), key=lambda k: S[A][k]); i = A
    par = {}
    while i > 0 and j > 0:
        if T[i][j] == 0:
            if sim(letra[i - 1][0], palavras[j - 1][0]) >= .6:
                par[i - 1] = j - 1
            i -= 1; j -= 1
        elif T[i][j] == 1: i -= 1
        else: j -= 1
    # tempo de cada linha = início da primeira palavra casada da linha
    inicio = [None] * len(linhas); casadas = [0] * len(linhas); total = [0] * len(linhas)
    for k, (_, li) in enumerate(letra):
        total[li] += 1
        if k in par:
            casadas[li] += 1
            if inicio[li] is None:
                inicio[li] = palavras[par[k]][1]
    return inicio, casadas, total


def main():
    linhas = linhas_da_letra(open(LETRA, encoding='utf-8').read())
    palavras = transcrever()
    json.dump(palavras, open(SAIDA + '.palavras.json', 'w', encoding='utf-8'), ensure_ascii=False)
    inicio, casadas, total = alinhar(linhas, palavras)
    # linhas sem casamento: interpola entre vizinhas; garante ordem crescente
    n = len(linhas)
    for i in range(n):
        if inicio[i] is not None and i > 0:
            ant = max((inicio[k] for k in range(i) if inicio[k] is not None), default=None)
            if ant is not None and inicio[i] < ant:
                inicio[i] = None
    conhecidos = [i for i in range(n) if inicio[i] is not None]
    for i in range(n):
        if inicio[i] is None and conhecidos:
            ant = [k for k in conhecidos if k < i]; dep = [k for k in conhecidos if k > i]
            if ant and dep:
                a, b = ant[-1], dep[0]; inicio[i] = round(inicio[a] + (inicio[b] - inicio[a]) * (i - a) / (b - a), 2)
            elif ant:
                inicio[i] = round(inicio[ant[-1]] + 3.0 * (i - ant[-1]), 2)
            else:
                inicio[i] = None
    json.dump(inicio, open(SAIDA, 'w'), separators=(',', ':'))
    ok = sum(1 for i in range(n) if total[i] and casadas[i] / total[i] >= .5)
    print(f'linhas: {n} · bem casadas: {ok} ({ok * 100 // max(1, n)}%)', file=sys.stderr)
    for i, l in enumerate(linhas):
        t = inicio[i]
        print(f"{'' if t is None else f'{int(t // 60)}:{t % 60:05.2f}':>8}  {casadas[i]}/{total[i]}  {l}", file=sys.stderr)


if __name__ == '__main__':
    main()
