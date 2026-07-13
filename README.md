# Sinal — Gerador de QR Codes (versão simples, sem histórico)

Cada pessoa que acessa gera o próprio QR code e baixa na hora. Nada fica salvo
em nenhum banco de dados — quando a página é fechada ou recarregada, some.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre em http://localhost:8501

## Publicar de graça (Streamlit Community Cloud)

1. Crie um repositório no GitHub e suba `app.py` e `requirements.txt`.
2. Entre em https://share.streamlit.io com sua conta GitHub.
3. Clique em "New app", escolha o repositório e o arquivo `app.py`.
4. Clique em "Deploy". Em 1-2 minutos o site está no ar, com um link tipo
   `sinal.streamlit.app`, pronto pra qualquer pessoa usar no PC ou celular.
