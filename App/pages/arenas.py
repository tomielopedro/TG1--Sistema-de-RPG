import streamlit as st
from pages.criar_arena import criar_arena
from utils.streamlit_utils import *

mostrar, criar = st.tabs(['Galeria de Arenas', 'Criar Arena'])
with st.sidebar:

    st.selectbox('Filtre por mapas', st.session_state.gerenciamento_arenas.mapas_dict.keys())
    st.selectbox('Filtre por tipo de jogo', st.session_state.gerenciamento_arenas.tipo_dict.keys())
with mostrar:
    st.title(f'Arenas Criadas: {len(st.session_state.arenas_lidas)}')
    cols = st.columns(2)
    personagens_mortos = []
    # Itera sobre os personagens lidos
    for i, arena in enumerate(st.session_state.arenas_lidas):
        col = cols[i % 2]  # Alterna entre coluna 0 e 1
        with col:
            criar_card_arena(arena)

with criar:
    criar_arena()


