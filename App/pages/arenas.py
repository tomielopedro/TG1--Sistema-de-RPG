import streamlit as st
from utils.page_functions.criar_arena import criar_arena
from utils.page_functions.galeria_arenas import criar_card_arena
from utils.streamlit_utils import set_background_as_frame

set_background_as_frame('assets/images/extras/fundo.png')
mostrar, criar = st.tabs(['Galeria de Arenas', 'Criar Arena'])
mapas = list(st.session_state.gerenciamento_arenas.mapas_dict.keys())
mapas = ['Todos'] + mapas
tipo_jogo = list(st.session_state.gerenciamento_arenas.tipo_dict.keys())
tipo_jogo = ['Todos'] + tipo_jogo

arenas_lidas = st.session_state.arenas_lidas
with st.sidebar:

    mapa_selecionado = st.selectbox('Filtre por mapas', mapas)
    if mapa_selecionado != 'Todos':
        arenas_lidas = [arena for arena in arenas_lidas if arena.mapa.nome_mapa == mapa_selecionado]
    tipo_selecionado = st.selectbox('Filtre por tipo de jogo', tipo_jogo)
    if tipo_selecionado != 'Todos':
        arenas_lidas = [arena for arena in arenas_lidas if arena.tipo_jogo == tipo_selecionado]
with mostrar:
    st.title(f'Arenas Criadas: {len(arenas_lidas)}')
    cols = st.columns(2)
    personagens_mortos = []
    # Itera sobre os personagens lidos
    for i, arena in enumerate(arenas_lidas):
        col = cols[i % 2]  # Alterna entre coluna 0 e 1
        with col:
            criar_card_arena(arena)

with criar:
    criar_arena()


