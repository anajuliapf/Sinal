const { getStore } = require('@netlify/blobs');

exports.handler = async (event) => {
  const code = event.queryStringParameters && event.queryStringParameters.code;

  if (!code) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Código não informado.' }) };
  }

  const store = getStore('sinal-links');
  const raw = await store.get(code);

  if (!raw) {
    return { statusCode: 404, body: JSON.stringify({ error: 'Código não encontrado.' }) };
  }

  const data = JSON.parse(raw);

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      destino: data.destino,
      tipo: data.tipo,
      label: data.label,
      updatedAt: data.updatedAt,
    }),
  };
};
