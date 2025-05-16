import streamlit as st
from utils.streamlit_utils import criar_card_personagem
import streamlit.components.v1 as components
from RPG import *


def mostrar_personagem():
    # Função para lançar dado com animação CSS
    def lancar_dado(dado):
        numero = dado.jogar()

        html_code = f"""
        <style>
        .dado {{
          width: 120px;
          height: 120px;
          border-radius: 10px;
          background: white;
          color: black;
          font-size: 48px;
          font-weight: bold;
          display: flex;
          justify-content: center;
          align-items: center;
          animation: girar 0.6s ease;
          margin: 20px auto;
          border: 3px solid #333;
        }}
        @keyframes girar {{
          0%   {{ transform: rotateY(0deg); }}
          50%  {{ transform: rotateY(180deg); }}
          100% {{ transform: rotateY(360deg); }}
        }}
        </style>
        <div class="dado">{numero}</div>
        """

        # Renderiza dado animado na interface
        components.html(html_code, height=200)
        return numero


    # Sidebar do app
    with st.sidebar:
        st.title('Sistema de RPG')
        st.divider()


    # Título principal da página com contador de personagens
    # Cria duas colunas para exibir personagens lado a lado
    cols = st.columns(2)
    personagens_mortos = []
    # Itera sobre os personagens lidos
    for i, personagem in enumerate(st.session_state.personagens_lidos):
        col = cols[i % 2]  # Alterna entre coluna 0 e 1
        with col:
            criar_card_personagem(personagem)
