const { getStore } = require('@netlify/blobs');

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

  const { code, destino, password } = body;

  if (!password || password !== process.env.SINAL_EDIT_PASSWORD) {
    return { statusCode: 401, body: JSON.stringify({ error: 'Senha incorreta.' }) };
  }
  if (!code || !destino) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Faltam campos obrigatórios.' }) };
  }

  const store = getStore('sinal-links');
  const raw = await store.get(code);

  if (!raw) {
    return { statusCode: 404, body: JSON.stringify({ error: 'Código não encontrado.' }) };
  }

  const data = JSON.parse(raw);
  data.destino = destino;
  data.updatedAt = new Date().toISOString();

  await store.set(code, JSON.stringify(data));

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ok: true, updatedAt: data.updatedAt }),
  };
};
