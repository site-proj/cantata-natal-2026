# Aba "Seu Olhar": como ligar o envio de fotos ao seu Google Drive

Faça isso uma vez, no computador, com a conta Google que tem o espaço livre (cerca de 10 minutos).
Os convidados **não** precisam de conta Google: só você.

## 1. Criar a pasta no Drive

1. Abra o [Google Drive](https://drive.google.com) e crie uma pasta, por exemplo **Cantata 2026 — Seu Olhar**.
2. Abra a pasta e copie o **ID** dela no endereço do navegador: é o trecho depois de `/folders/`.
   Exemplo: em `https://drive.google.com/drive/folders/1AbC2dEf3GhI`, o ID é `1AbC2dEf3GhI`.
3. **Não** compartilhe a pasta com ninguém. Ela continua privada.

## 2. Criar o script

1. Abra [script.google.com](https://script.google.com) e clique em **Novo projeto**.
2. Clique em "Projeto sem título" e dê o nome **Cantata — Seu Olhar**.
3. Apague todo o código que aparece e cole o conteúdo do arquivo `seu-olhar-apps-script.gs`.
4. Na linha `const PASTA_ID = 'COLE_AQUI_O_ID_DA_PASTA';`, troque `COLE_AQUI_O_ID_DA_PASTA` pelo ID que você copiou (mantenha as aspas).
5. Clique em **Salvar** (ícone de disquete).
6. **Permissão de gravação no Drive** (sem isso o Drive recusa os envios com "insufficient authentication scopes"):
   1. Clique em **Configurações do projeto** (engrenagem, na coluna da esquerda) e marque
      **Mostrar arquivo de manifesto "appsscript.json" no editor**.
   2. Volte ao **Editor** (ícone `< >`), abra o arquivo **appsscript.json**, apague tudo e cole o conteúdo de
      `seu-olhar-appsscript.json`. Salve.

## 3. Autorizar (uma vez)

1. Na barra de cima, escolha a função **autorizar** e clique em **Executar**.
2. Vai aparecer "Autorização necessária": clique em **Revisar permissões** e escolha a sua conta.
3. O Google vai avisar que "o app não foi verificado". Isso é normal, porque o script é seu e não foi publicado para outras pessoas:
   clique em **Avançado** e depois em **Acessar Cantata — Seu Olhar (não seguro)**.
4. Clique em **Permitir**. No registro de execução deve aparecer "Autorizado. Pasta: Cantata 2026 — Seu Olhar".

## 4. Publicar o script

1. Clique em **Implantar → Nova implantação**.
2. Na engrenagem ao lado de "Selecionar tipo", escolha **App da Web**.
3. Preencha:
   - **Descrição:** Seu Olhar
   - **Executar como:** Eu (seu e-mail)
   - **Quem pode acessar:** Qualquer pessoa
4. Clique em **Implantar** e copie o **URL do app da Web** (termina em `/exec`).
5. **Envie esse link para o Claude.** Ele não dá acesso à sua conta; só permite pedir envios para aquela pasta, com as regras do script.

## 5. Testar

Depois que o link estiver no site:

1. No celular, abra o site com `?teste=1` no endereço:
   `https://site-proj.github.io/cantata-natal-2026/?teste=1#seu-olhar`
2. Envie uma foto e um vídeo curto e confira se chegaram na pasta do Drive.
3. Apague os arquivos de teste da pasta.

## 6. Desligar o modo de teste (importante)

1. No script, troque `const MODO_TESTE = true;` por `const MODO_TESTE = false;` e salve.
2. Clique em **Implantar → Gerenciar implantações**, no lápis (editar), em **Versão** escolha **Nova versão** e clique em **Implantar**.
   O link continua o mesmo; não precisa mandar de novo.

A partir daí, o envio só funciona de **18/12 às 00:00 até 20/12 às 23:59** (horário de Brasília), mesmo que alguém use `?teste=1`.

## Regras do envio

- Só fotos e vídeos, até **300 MB por arquivo**.
- O nome do arquivo no Drive fica assim: `2026-12-18 20.15.03 - Ana Souza - IMG_1234.jpg`.
- Quem envia não vê nem apaga o que os outros enviaram.
