import streamlit as st
from utils.page_functions.criar_arena import criar_arena
from utils.page_functions.galeria_arenas import criar_card_arena
from utils.streamlit_utils import set_background_as_frame
from utils.streamlit_utils import get_image_path
from utils.streamlit_utils import exibir_logs_chat_generico


""" 
Interface principal da aplicação Streamlit para gerenciamento de arenas.
Permite visualizar arenas existentes, criar novas arenas e acessar logs de atividades.

Funcionalidades principais:
- Exibição de uma galeria com arenas já criadas, com filtros por mapa e tipo de jogo.
- Criação de novas arenas por meio de formulário interativo.
- Acesso aos logs de ações realizadas com as arenas.

Dependências:
- Funções auxiliares localizadas em utils/page_functions e utils/streamlit_utils.
"""


set_background_as_frame(get_image_path('assets/images/extras/fundo.png'))
mostrar, criar, logs = st.tabs(['Galeria de Arenas', 'Criar Arena', 'Logs'])
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
    c1, c2 = st.columns([3, 1])
    c1.title(f'Arenas Criadas: {len(arenas_lidas)}')
    with open('data/arenas.txt', "rb") as f:
        c2.download_button(
            label="📥 Baixar Arquivo de Arenas",
            data=f,
            file_name='data/arenas.txt'.split("/")[-1],
            mime="text/plain"
        )

    cols = st.columns(2)
    personagens_mortos = []
    # Itera sobre os personagens lidos
    for i, arena in enumerate(arenas_lidas):
        col = cols[i % 2]  # Alterna entre coluna 0 e 1
        with col:
            criar_card_arena(arena)

with criar:
    criar_arena()

with logs:
    exibir_logs_chat_generico("data/logs_arena.txt", titulo="🏟️ Logs de Arenas")



