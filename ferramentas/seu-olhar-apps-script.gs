/**
 * Cantata de Natal 2026 — aba "Seu Olhar"
 * Recebe fotos e vídeos dos convidados direto numa pasta do Google Drive,
 * sem que eles precisem de conta Google.
 *
 * Como funciona: o site pede a este script um "link de envio" para cada arquivo.
 * O script confere o tipo, o tamanho e o período, e cria esse link no Google Drive
 * (vale só para aquele arquivo, naquela pasta). O celular do convidado envia o
 * arquivo em partes direto para o Drive. Este script nunca entrega o acesso à
 * sua conta ao site.
 *
 * Passo a passo de instalação: veja o arquivo "seu-olhar-instalacao.md".
 */

// 1) Cole aqui o ID da pasta do Drive (o trecho do link depois de /folders/).
const PASTA_ID = 'COLE_AQUI_O_ID_DA_PASTA';

// 2) Durante o teste, deixe true. Depois do teste, troque para false e atualize a implantação.
const MODO_TESTE = true;

// Período de envio (horário de Brasília): 18/12/2026 00:00 até 20/12/2026 23:59.
const INICIO = new Date('2026-12-18T00:00:00-03:00');
const FIM = new Date('2026-12-21T00:00:00-03:00');

// Limites.
const TAMANHO_MAXIMO = 300 * 1024 * 1024; // 300 MB por arquivo
const ORIGENS_PERMITIDAS = ['https://site-proj.github.io'];
const EXTENSOES = ['jpg', 'jpeg', 'png', 'heic', 'heif', 'webp', 'gif', 'mp4', 'mov', 'm4v', '3gp', 'webm', 'avi'];

function doGet(e) {
  const p = (e && e.parameter) || {};
  try {
    if (p.acao === 'status') return responder({ ok: true, aberto: estaAberto() });
    if (p.acao !== 'iniciar') return responder({ ok: false, erro: 'acao' });
    if (!estaAberto()) return responder({ ok: false, erro: 'fechado' });

    const origem = String(p.origem || '');
    if (ORIGENS_PERMITIDAS.indexOf(origem) < 0) return responder({ ok: false, erro: 'origem' });

    const tamanho = Number(p.tamanho);
    if (!(tamanho > 0) || tamanho > TAMANHO_MAXIMO) return responder({ ok: false, erro: 'tamanho' });

    const original = String(p.arquivo || 'arquivo').slice(0, 120);
    const extensao = (original.split('.').pop() || '').toLowerCase();
    let tipo = String(p.tipo || '');
    const tipoOk = /^(image|video)\//.test(tipo);
    if (!tipoOk && EXTENSOES.indexOf(extensao) < 0) return responder({ ok: false, erro: 'tipo' });
    if (!tipoOk) tipo = 'application/octet-stream';

    const nome = limpar(String(p.nome || '')).slice(0, 40) || 'Convidado';
    const quando = Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'yyyy-MM-dd HH.mm.ss');
    const nomeFinal = quando + ' - ' + nome + ' - ' + limpar(original);

    // Garante que a pasta existe (e que o script tem permissão no Drive).
    DriveApp.getFolderById(PASTA_ID);

    const resposta = UrlFetchApp.fetch(
      'https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true',
      {
        method: 'post',
        contentType: 'application/json; charset=UTF-8',
        headers: {
          Authorization: 'Bearer ' + ScriptApp.getOAuthToken(),
          'X-Upload-Content-Type': tipo,
          'X-Upload-Content-Length': String(tamanho),
          // Libera o envio a partir do navegador, só para a origem do site.
          Origin: origem
        },
        payload: JSON.stringify({ name: nomeFinal, parents: [PASTA_ID] }),
        muteHttpExceptions: true
      }
    );
    const link = resposta.getHeaders()['Location'] || resposta.getHeaders()['location'];
    if (resposta.getResponseCode() !== 200 || !link) {
      // Devolve o motivo (sem dados da conta) para facilitar o diagnóstico.
      return responder({ ok: false, erro: 'drive', codigo: resposta.getResponseCode(), detalhe: resposta.getContentText().slice(0, 400) });
    }
    return responder({ ok: true, link: link });
  } catch (erro) {
    return responder({ ok: false, erro: 'interno', detalhe: String(erro).slice(0, 300) });
  }
}

function estaAberto() {
  if (MODO_TESTE) return true;
  const agora = new Date();
  return agora >= INICIO && agora < FIM;
}

function limpar(texto) {
  return texto.replace(/[\\/:*?"<>|\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
}

function responder(objeto) {
  return ContentService.createTextOutput(JSON.stringify(objeto)).setMimeType(ContentService.MimeType.JSON);
}

// Rode esta função uma vez pelo editor para autorizar o acesso ao Drive.
function autorizar() {
  DriveApp.getFolderById(PASTA_ID);
  UrlFetchApp.fetch('https://www.googleapis.com/discovery/v1/apis/drive/v3/rest', { muteHttpExceptions: true });
  Logger.log('Autorizado. Pasta: ' + DriveApp.getFolderById(PASTA_ID).getName());
}
