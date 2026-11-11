# Karaokê das letras — como foi feito (e o que deu errado)

## Arquivos
- `letras/<driveId>.txt` — letra/cifra em texto, extraída com `ferramentas/extrair-letras.py`
  (`pdftotext -layout`, detecção de duas colunas, XML de DOCX; PDF de imagem é transcrito à mão).
- `letras/<driveId>.tempos.json` — lista com o tempo (s) de início de cada linha da letra
  exibida, na mesma ordem; `null` para linha que não é cantada naquele ponto.
- `ferramentas/sincronizar-letra.py` — gera os tempos:
  `python ferramentas/sincronizar-letra.py <audio.mp3> <letra.txt> <saida.tempos.json> [modelo]`

## Método aprovado
1. Reconhecimento com **faster-whisper `small`**, int8 em CPU, `word_timestamps=True`,
   `language='pt'`, **`vad_filter=False`** (com VAD só reconhecia ~14 palavras).
2. Áudio decodificado com ffmpeg para PCM float32 16 kHz e passado como array
   (evita erro `metadata_errors` do PyAV).
3. Alinhamento tipo Needleman-Wunsch dos tokens da letra contra as palavras reconhecidas,
   com início e fim livres; linhas sem par são interpoladas. Sincronização em blocos para
   refrões repetidos (a linha acende em **cada** repetição).
4. Revisão manual de trechos difíceis: pontes repetidas, testemunho falado, partes
   instrumentais. Reconheça de novo só o trecho com prompt e ajuste à mão buscando a linha
   **pelo texto**, não pelo índice (erro de deslocamento já aconteceu).
5. Confira a ordem crescente dos tempos e verifique no navegador, em segundos de amostra,
   se a linha certa está acesa.

## Ambiente
- Download do modelo: `HF_HUB_DISABLE_XET=1` e `HF_HOME` no scratchpad; hosts do Hugging
  Face liberados no ambiente.

## Armadilhas
- ffmpeg `apad` sem limite criou um WAV de 28 GB e encheu o disco — use concat de
  segmentos (`-ss`/`-t`) em vez disso. `amix` gerou áudio vazio; use concat.
- `recordVideo` do Playwright deu quadros cinza; para vídeo de demonstração, capture
  screenshots em loop e monte com o concat demuxer usando as durações reais.
