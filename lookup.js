const { getStore } = require('@netlify/blobs');
const crypto = require('crypto');

// Sem caracteres ambíguos (0/O, 1/l/I) pra facilitar digitar o código na mão
const CHARS = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789';

function generateCode(len = 7) {
  let out = '';
  for (let i = 0; i < len; i++) {
    out += CHARS[crypto.randomInt(0, CHARS.length)];
  }
  return out;
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Método não permitido.' }) };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, body: JSON.stringify({ error: 'JSON inválido.' }) };
  }

  const { destino, tipo, label, password } = body;

  if (!password || password !== process.env.SINAL_EDIT_PASSWORD) {
    return { statusCode: 401, body: JSON.stringify({ error: 'Senha incorreta.' }) };
  }
  if (!destino || !tipo) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Faltam campos obrigatórios.' }) };
  }

  const store = getStore('sinal-links');

  let code;
  for (let attempts = 0; attempts < 6; attempts++) {
    const candidate = generateCode();
    const existing = await store.get(candidate);
    if (!existing) {
      code = candidate;
      break;
    }
  }
  if (!code) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Não foi possível gerar um código único, tente de novo.' }) };
  }

  const record = {
    destino,
    tipo,
    label: label || '',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  await store.set(code, JSON.stringify(record));

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  };
};
