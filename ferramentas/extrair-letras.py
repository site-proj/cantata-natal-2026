"""Extrai letras e cifras (PDF/DOCX do Drive) para texto limpo, uma coluna, pronto para o player."""
import re, subprocess, sys, zipfile, os
from xml.etree import ElementTree as ET

LIXO = [
    re.compile(r'^\s*\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}'),          # cabeçalho de impressão do navegador
    re.compile(r'\(Impress[ãa]o\)', re.I),
    re.compile(r'https?://|www\.|\.com(\.br)?/', re.I),
    re.compile(r'^\s*\d+\s*/\s*\d+\s*$'),                                    # 1/2
    re.compile(r'^\s*P[áa]gina\s+\d+', re.I),
    re.compile(r'cifra\s*club|letras\.mus|letras\.com', re.I),
]


def pagina_layout(pdf, n):
    return subprocess.run(['pdftotext', '-layout', '-f', str(n), '-l', str(n), pdf, '-'], capture_output=True, text=True).stdout


def paginas(pdf):
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    m = re.search(r'Pages:\s+(\d+)', info)
    return int(m.group(1)) if m else 1


def separar_colunas(linhas):
    """Se a página tem duas colunas de texto, devolve esquerda + direita; senão, as linhas como estão.
    Linhas largas que atravessam o meio (título, rodapé "Composição: …") ficam inteiras no lugar certo."""
    cheias = [l for l in linhas if l.strip()]
    if len(cheias) < 6:
        return linhas
    larg = max(len(l) for l in cheias)
    tolera = max(2, int(len(cheias) * .1))
    candidatos = []
    for c in range(int(larg * .3), int(larg * .72)):
        cruza = [l for l in cheias if len(l) > c - 1 and l[c - 1:c + 2].strip()]
        if len(cruza) > tolera:
            continue
        direita = sum(1 for l in cheias if l not in cruza and l[c + 2:].strip())
        esquerda = sum(1 for l in cheias if l not in cruza and l[:c - 1].strip())
        if direita >= len(cheias) * .3 and esquerda >= len(cheias) * .3:
            candidatos.append((len(cruza), c))
    # o melhor vão é o que corta menos linhas; entre os empatados, o do meio do vão
    if candidatos:
        menor = min(n for n, _ in candidatos)
        cs = [c for n, c in candidatos if n == menor]
        melhor = cs[len(cs) // 2]
    else:
        melhor = None
    if melhor is None:
        return linhas
    c = melhor
    ultima_dir = max(i for i, l in enumerate(linhas) if l[c + 2:].strip() and not l[c - 1:c + 2].strip())
    esq, dir_, rodape = [], [], []
    for i, l in enumerate(linhas):
        if len(l) > c - 1 and l[c - 1:c + 2].strip():      # atravessa o meio
            (rodape if i > ultima_dir else esq).append(l.strip())
            continue
        esq.append(l[:c].rstrip()); dir_.append(l[c:].strip())
    return esq + [''] + dir_ + [''] + rodape


def limpar(linhas):
    out = []
    for l in linhas:
        if any(p.search(l) for p in LIXO):
            continue
        out.append(l.rstrip())
    # junta quebras "órfãs" (palavra solta que é continuação da linha anterior), comum em colunas estreitas
    juntas = []
    for l in out:
        if juntas and l.strip() and len(l.strip().split()) == 1 and l.strip()[0].islower() and juntas[-1].strip() and not juntas[-1].rstrip().endswith(('.', '!', '?', ':')):
            juntas[-1] = juntas[-1].rstrip() + ' ' + l.strip()
        else:
            juntas.append(l)
    texto = '\n'.join(juntas)
    texto = re.sub(r'\n{3,}', '\n\n', texto).strip('\n')
    return texto + '\n'


def de_pdf(pdf, cifra):
    todas = []
    for n in range(1, paginas(pdf) + 1):
        ls = pagina_layout(pdf, n).replace('\f', '').split('\n')
        if not cifra:
            ls = separar_colunas(ls)
            ls = [l.strip() for l in ls]
        todas += ls + ['']
    if cifra:   # remove recuo comum da cifra sem perder o alinhamento entre acordes e letra
        cheias = [l for l in todas if l.strip()]
        recuo = min((len(l) - len(l.lstrip(' ')) for l in cheias), default=0)
        todas = [l[recuo:] for l in todas]
    return limpar(todas)


def de_docx(path):
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    xml = zipfile.ZipFile(path).read('word/document.xml')
    raiz = ET.fromstring(xml)
    linhas = []
    for p in raiz.iter('{%s}p' % ns['w']):
        partes = []
        for no in p.iter():
            tag = no.tag.split('}')[1]
            if tag == 't':
                partes.append(no.text or '')
            elif tag == 'tab':
                partes.append('    ')
            elif tag == 'br':
                partes.append('\n')
        linhas += ''.join(partes).split('\n')
    return limpar(linhas)


if __name__ == '__main__':
    arq, tipo = sys.argv[1], sys.argv[2]
    with open(arq, 'rb') as f:
        cab = f.read(4)
    print(de_docx(arq) if cab[:2] == b'PK' else de_pdf(arq, tipo == 'cifra'), end='')
