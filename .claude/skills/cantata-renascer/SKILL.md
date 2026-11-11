---
name: cantata-renascer
description: Padrões aprovados (e o que foi reprovado) para o site, as artes e os vídeos da Cantata de Natal 2026 "Quando o Céu Tocou a Terra", da Renascer Jundiaí. Use sempre que for mexer no site (index.html, abas Abertura, Figurino, Seu Olhar, Ensaios, letras/karaokê), criar artes ou vídeos de divulgação da cantata, ou publicar alterações no GitHub Pages.
---

# Cantata Renascer

Guia destilado das conversas em que o site da Cantata de Natal 2026 foi construído.
Tudo aqui foi **aprovado** ou **reprovado** explicitamente pelo responsável. Siga o
aprovado e não repita o reprovado.

## 1. Como trabalhar com o responsável

- **Responda em português**, curto e direto. A pessoa acompanha pelo celular (Android).
- **Mostre antes de aplicar** quando a mudança é visual: uma amostra, um print, um vídeo
  curto ou o HTML de preview. Ela pede "posso ver antes?" com frequência; antecipe-se.
- Quando ela diz **"Pode fazer" / "Aprovado" / "Perfeito"**, execute o plano inteiro que
  foi proposto (inclusive publicar, se o plano dizia isso) sem perguntar de novo.
- Ela prefere **autonomia**: não peça confirmações intermediárias desnecessárias; quando
  pedir "faça para todas", aplique em todos os itens (ex.: as 9 músicas) de uma vez.
- Ao perguntar "é possível?", responda com níveis de solução (simples → completo), diga
  qual recomenda e o que testa antes de mostrar.
- Ela **testa no celular** depois de publicar. Garanta que funciona em tela pequena
  primeiro, depois no desktop/TV.
- Ao terminar uma publicação, diga **se já está no ar** (ela sempre pergunta).

## 2. Fluxo de publicação (aprovado)

1. Desenvolva no branch de trabalho da sessão; nunca direto em `main`.
2. Commits em português, título curto com a área na frente: `Ensaios: ...`,
   `Seu Olhar: ...`, `Abertura: ...`, `Figurino: ...`. Corpo com bullets do que muda.
   Enquanto não aprovado, termine com `(Ainda não publicado: aguardando aprovação.)`.
3. Com aprovação: abra PR para `main` e faça o merge (ela autoriza "abra o PR e mescle").
4. O workflow `.github/workflows/pages.yml` publica `main` no GitHub Pages. **Acompanhe o
   deploy até `success`.** Se travar no passo "Deploy to GitHub Pages", cancele e rode o
   workflow de novo (`workflow_dispatch` em `main`).
5. Depois do deploy, avise que está publicado e o que testar.
6. Link definitivo é o do Pages em produção — nunca passe URL de teste/preview como final.

## 3. Identidade visual (aprovada)

- Tema: **noite de Natal, escuro e dourado**, presépio/manjedoura ao fundo.
- Cores (tokens em `index.html`): `--night #100d0a`, `--panel #19130e`,
  `--gold #dfbb77`, `--ivory #f4ead5`, `--muted #c3b9a8`, `--line rgba(223,187,119,.24)`.
  Destaque de karaokê: `#ffe9b8` com brilho dourado.
- Fontes: **Cinzel** (títulos, maiúsculas, dourado metálico), **Cormorant Garamond
  itálico** (palavras de ligação/poéticas), **DM Sans** (texto e interface).
- Título oficial: "Quando o Céu Tocou a Terra" · "Cantata de Natal 2026" · Renascer
  Jundiaí. Logos em `images/` (renascer, louvor, dança, kids, teen, mídias).
- Artes e vídeos de divulgação **usam essa identidade** (fontes, cores, presépio e logo).
  Não invente outra estética.

## 4. Decisões por área

### Abertura (página inicial)
- ✅ **Tipografia cinética** palavra por palavra: "quando o" e "tocou a" em Cormorant
  itálico digitados saindo do desfoque; "CÉU" em Cinzel dourado grande entrando com
  desfoque de movimento e parando firme (a estrela pulsa); "Terra" escrita depois e o
  presépio se revela. Respeita `prefers-reduced-motion` (título direto).
- ❌ Título em **faixas horizontais + fio de luz** descendo da estrela — reprovado.
- ❌ Inspiração no estilo "showreel" genérico (prompt-motion) — não gostou.
- ❌ **"Salto" ao rolar** (efeito de tela cheia / mudança de altura do hero no celular) —
  pediu para remover; visualmente estranho. Use altura estável (`svh`).
- O título termina na mesma altura de antes no celular; o botão "Sobre a Cantata" não
  pode encostar nas figuras. Remova assets não usados (PNGs antigos).

### Figurino
- ✅ Imagem modelo com as pessoas; **tocar numa pessoa a traz para frente**.
- ✅ Recorte com **borda iluminada** em volta da pessoa para disfarçar falhas do recorte.
- ✅ Ao abrir, um **quadro com a descrição ao lado da pessoa** (no celular a descrição não
  pode ficar lá embaixo, fora da vista).
- ✅ **Cada pessoa abre e fecha sozinha**; para abrir outra, toca-se nela.
- ✅ Destaque visual convidando a tocar nas imagens.
- ❌ Recorte com falhas no chão/na pessoa e pessoas saindo do enquadramento ao voltar.

### Seu Olhar (envio de fotos e vídeos dos convidados)
- Nome escolhido: **"Seu Olhar"** (não "Pelos Seus Olhos").
- Destino: pasta do Google Drive via Apps Script (`ferramentas/seu-olhar-*`). O script
  precisa ser da **conta dona da pasta**, com escopo de gravação no Drive.
- ✅ Botão de escolher arquivos **bloqueado com contagem regressiva ao vivo** até 18/12;
  envio aberto **de 18 a 20/12** — o texto deve deixar claro que dá para enviar **até 20/12**.
- ✅ Ao terminar o envio, a barra de carregamento some e aparece uma **tela de confirmação**.
- ✅ Limite de **300 MB** por arquivo; erros do Drive mostrados de forma detalhada.
- ❌ Limite de 1 GB (grande demais). ❌ Dica "use o Wi-Fi da igreja".

### Ensaios (player de músicas, letras e cifras)
- ✅ As 9 músicas como **cartões** (capa dourada, nome, artista, play); tocar abre um
  **player que cresce a partir do cartão**; **arrastar para o lado troca de música**;
  fecha com ×, arrastando para baixo ou Esc; controles na tela de bloqueio.
- ✅ Letra e cifra como **texto de verdade** (`letras/<driveId>.txt`), nunca o PDF encolhido.
  Abas Ouvir / Letra / Cifra / Original; o modo vale para todas ao arrastar.
- ✅ **Letra grande** (ela pediu maior ainda) no player e no telão; A−/A+ salvo no aparelho.
- ✅ Letra **sem linhas de acordes** quando a música só tem cifra, **sem rótulos de seção**
  (Refrão, Ponte, Intro…) e sem notas soltas.
- ✅ **Seguir a música** (♪, ligado por padrão): rola conforme o áudio; rolar com o dedo
  pausa 5 s.
- ✅ **Modo telão** (⛶): tela cheia, letra enorme, foco no centro, controles discretos.
- ✅ **Karaokê nas 9 músicas**: a linha cantada acende e fica centralizada, inclusive em
  cada repetição do refrão (`letras/<id>.tempos.json`). Detalhes técnicos em
  [references/karaoke.md](references/karaoke.md).
- ❌ Player antigo com PDF pequeno e difícil de enxergar.

### Artes e vídeos de divulgação
- ✅ Contagem regressiva em vídeo (a partir de 37 dias para trás) **com a identidade da
  cantata**.
- ✅ Artes 16:9 ("Faça parte do coral", "Grande Coral") com **texto centralizado**, as
  fontes da identidade, a arte inteira em 16:9.
- ✅ **Logo/título principal grande** e **mensagens de baixo grandes e legíveis**, mesmo
  que fiquem um pouco sobre a manjedoura. "JUNDIAÍ" sempre legível.
- ❌ Título e mensagens pequenos para não cobrir o presépio.

## 5. Checklist antes de mostrar qualquer coisa

- [ ] Testado em viewport de celular (≈390 px) e desktop; sem rolagem horizontal.
- [ ] Sem "saltos" de layout ao rolar ou ao abrir/fechar elementos.
- [ ] Cores, fontes e tom dourado da identidade.
- [ ] Textos em português, datas no formato dd/mm.
- [ ] Movimento reduzido respeitado em animações.
- [ ] Print ou vídeo curto pronto para enviar junto com a explicação.
