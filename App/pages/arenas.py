import streamlit as st
from utils.page_functions.criar_arena import criar_arena
from utils.page_functions.galeria_arenas import criar_card_arena
from utils.caminhos import get_image_path
from utils.logs import exibir_logs_chat_generico
from utils.visual import background
from utils.visual import set_background_as_frame


# === Plano de fundo da aplicação ===
if st.toggle('Ativar Container', True):
    set_background_as_frame(get_image_path('assets/images/extras/fundo.png'))
else:
    background(get_image_path('assets/images/extras/fundo.png'))

# === Criação das abas da página ===
mostrar, criar, logs = st.tabs(['Galeria de Arenas', 'Criar Arena', 'Logs'])

# === Recupera os mapas e tipos de jogo disponíveis no sistema ===
mapas = list(st.session_state.gerenciamento_arenas.mapas_dict.keys())
mapas = ['Todos'] + mapas

tipo_jogo = list(st.session_state.gerenciamento_arenas.tipo_dict.keys())
tipo_jogo = ['Todos'] + tipo_jogo

# === Carrega arenas existentes do session state ===
arenas_lidas = st.session_state.arenas_lidas

with st.sidebar:
    mapa_selecionado = st.selectbox('Filtre por mapas', mapas)
    tipo_selecionado = st.selectbox('Filtre por tipo de jogo', tipo_jogo)

arenas_filtradas = st.session_state.arenas_lidas

if mapa_selecionado != 'Todos':
    arenas_filtradas = [
        arena for arena in arenas_filtradas
        if arena.mapa.nome_mapa == mapa_selecionado
    ]

if tipo_selecionado != 'Todos':
    arenas_filtradas = [
        arena for arena in arenas_filtradas
        if arena.tipo_jogo == tipo_selecionado
    ]

# === Aba "Galeria de Arenas" ===
with mostrar:
    c1, c2 = st.columns([3, 1])

    # Título e botão de download do arquivo de arenas
    c1.title(f'Arenas Criadas: {len(arenas_lidas)}')
    with open('data/arenas.txt', "rb") as f:
        c2.download_button(
            label="📥 Baixar Arquivo de Arenas",
            data=f,
            file_name='arenas.txt',
            mime="text/plain"
        )

    # Criação dos cards de arena em colunas
    cols = st.columns(2)
    for i, arena in enumerate(arenas_lidas):
        col = cols[i % 2]  # Alterna entre colunas para disposição visual
        with col:
            criar_card_arena(arena)

# === Aba "Criar Arena" ===
with criar:
    criar_arena()

# === Aba "Logs de Arenas" ===
with logs:
    exibir_logs_chat_generico("data/logs_arena.txt", titulo="🏟️ Logs de Arenas")
