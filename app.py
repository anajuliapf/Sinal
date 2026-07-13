import streamlit as st
import qrcode
from io import BytesIO
import re

st.set_page_config(page_title="Sinal — Gerador de QR Codes", page_icon="🔗", layout="centered")

# --- Estilo ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

.sinal-header {
    text-align: center;
    border-bottom: 1px solid #ddd8c8;
    padding-bottom: 18px;
    margin-bottom: 32px;
}
.sinal-title {
    font-family: 'Fraunces', serif; font-weight: 600; font-size: 38px; color: #14172b;
}
.sinal-title span { color: #c8922f; }
.sinal-tag {
    font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;
    letter-spacing: 0.12em; color: #3a3f5c; margin-top: 4px;
}

.qr-frame {
    border: 1px solid #ddd8c8; background: #fff; padding: 28px; text-align: center;
    margin-top: 24px;
}

.stButton>button, .stDownloadButton>button {
    background-color: #14172b; color: #faf9f5; border-radius: 2px; border: none;
    font-weight: 600; width: 100%;
}
.stButton>button:hover, .stDownloadButton>button:hover { background-color: #c8922f; color: #14172b; }

.url-display {
    font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #3a3f5c;
    word-break: break-all; text-align: center; margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sinal-header">
    <div class="sinal-title">Sinal<span>.</span></div>
    <div class="sinal-tag">Link → Código → Redirecionamento</div>
</div>
""", unsafe_allow_html=True)


def normalize_url(raw: str) -> str:
    raw = raw.strip()
    if not re.match(r"^https?://", raw, re.IGNORECASE):
        raw = "https://" + raw
    return raw


def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,}|"
        r"localhost|"
        r"\d{1,3}(?:\.\d{1,3}){3})"
        r"(?::\d+)?(?:/?|[/?]\S+)$", re.IGNORECASE)
    return bool(pattern.match(url))


def make_qr_png(url: str, box_size: int = 10) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#14172b", back_color="#ffffff")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


url_input = st.text_input("Link de destino", placeholder="https://exemplo.com/pagina-ou-redirecionamento")

c1, c2 = st.columns(2)
with c1:
    label_input = st.text_input("Nome do arquivo (opcional)", placeholder="Ex: cardapio, instagram")
with c2:
    size_choice = st.selectbox("Tamanho", ["Padrão", "Grande", "Impressão"], index=0)
size_map = {"Padrão": 8, "Grande": 14, "Impressão": 22}

generate = st.button("Gerar QR code", use_container_width=True)

if generate:
    if not url_input.strip():
        st.error("Digite um link para gerar o código.")
    else:
        normalized = normalize_url(url_input)
        if not is_valid_url(normalized):
            st.error("Esse link não parece válido. Verifique e tente novamente.")
        else:
            png_bytes = make_qr_png(normalized, box_size=size_map[size_choice])
            st.session_state["qr"] = png_bytes
            st.session_state["url"] = normalized
            st.session_state["filename"] = (
                re.sub(r"[^a-z0-9]+", "-", label_input.strip().lower()).strip("-") or "qrcode"
            )

if "qr" in st.session_state:
    st.markdown('<div class="qr-frame">', unsafe_allow_html=True)
    st.image(st.session_state["qr"], use_container_width=True)
    st.markdown(f'<div class="url-display">{st.session_state["url"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "Baixar PNG",
        data=st.session_state["qr"],
        file_name=f"{st.session_state['filename']}.png",
        mime="image/png",
        use_container_width=True,
    )
