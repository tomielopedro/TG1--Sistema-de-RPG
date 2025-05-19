import streamlit as st
import base64
from utils.streamlit_utils import get_image_path

"""
Tela inicial do jogo interativo em Streamlit.

Esta página define:
- Um fundo visual usando CSS com imagem base64.
- Uma animação central em Lottie.
- Um botão “Iniciar Jogo” que leva à tela de escolha de personagens.

Arquivo: pagina_inicial.py
"""


def get_image_base64(path):
    """
    Converte uma imagem localizada em `path` para uma string codificada em base64.

    Args:
        path (str): Caminho para a imagem.

    Returns:
        str: Imagem codificada em base64, pronta para ser usada em CSS como plano de fundo.
    """
    
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

background_image = get_image_base64(get_image_path("assets/images/extras/fundo_tela_inicial.png"))

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{background_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    div.stButton > button {{
        display: block;
        margin: 0 auto;
        background-color: #9D711D;
        color: white;
        padding: 12px 30px;
        font-size: 20px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
    }}
    
    .st-emotion-cache-h4xjwg {{
        height: 0rem;
    }}
    div.stButton > button:hover {{
        background-color: #b9811d;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)


st.components.v1.html("""
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<dotlottie-player src="https://lottie.host/6faab81e-b703-468a-b537-78b78acea1bc/oRgbqTQby6.lottie"
                  background="transparent"
                  speed="1"
                  style="width: 700px; height: 500px"
                  loop autoplay>
</dotlottie-player>
""", height=550)


st.markdown("<div style='text-align:center; padding-top: 20px;'>", unsafe_allow_html=True)
if st.button("▶ Iniciar Jogo"):
    st.session_state.mostrar_sidebar = True
    st.switch_page('pages/personagens.py')
st.markdown("</div>", unsafe_allow_html=True)
