import base64
import streamlit as st
from utils.caminhos import get_image_path, get_image_base64


def background(image_path: str):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background: url("data:image/png;base64,{encoded}") no-repeat center center fixed;
                background-size: cover;
            }}
            
            .st-emotion-cache-h4xjwg {{
                height: 0rem;
            }}
            </style>
        """, unsafe_allow_html=True)

def set_background_as_frame(image_path: str):
    """
    Define uma imagem como plano de fundo da aplicação Streamlit
    usando CSS inline com imagem codificada em Base64.

    Args:
        image_path (str): Caminho do arquivo de imagem (ex: "assets/images/fundo.png").
    """
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            div[data-testid="stVerticalBlock"] {{
                padding-top: 0rem !important;
            }}
            .block-container {{
                background-color: #101414;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 0 0px rgba(0, 0, 0, 0.1);
                margin-top: 5rem;
            }}
            .st-emotion-cache-h4xjwg,
            .st-emotion-cache-12fmjuu {{
                height: 0rem;
            }}
            .stApp {{
                background: url("data:image/png;base64,{encoded}") no-repeat center center fixed;
                background-size: cover;
            }}
            </style>
        """, unsafe_allow_html=True)


def exibir_avatar(personagem, morto=False) -> dict:
    image_path = get_image_path("assets/images/extras/morte.png") if morto else personagem.classe.foto
    image_base64 = get_image_base64(image_path)
    image_url = f"data:image/png;base64,{image_base64}"
    caption = (
        f'{personagem.classe.nome} ⚰️(Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})'
        if morto else
        f'{personagem.classe.nome} (Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})'
    )
    return {
        "url": image_url,
        "size": 60,
        "title": personagem.nome,
        "caption": caption,
        "key": f"{'morto' if morto else 'vivo'}_{personagem.nome}"
    }
