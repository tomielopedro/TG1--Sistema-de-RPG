import streamlit as st
from RPG import *
from utils.gerenciamento.GerenciamentoPersonagens import GerenciamentoPersonagens
from utils.gerenciamento.GerenciamentoArenas import GerenciamentoArenas



# === DICIONÁRIOS DE CLASSES, HABILIDADES, MAPAS, TIPOS DE JOGO ===
classes_dict = {
    'Mago': Mago(),
    'Guerreiro': Guerreiro(),
    'Ladino': Ladino()
}

habilidades_dict = {
    'BolaDeFogo': BolaDeFogo(),
    'Cura': Cura(),
    'TiroDeArco': TiroDeArco()
}

mapas_dict = {
    'Vilarejo': Vilarejo(),
    'Torre': Torre(),
}

tipos_jogo = {
    'X1': X1(),
    'PVP': PVP()
}

if "mostrar_sidebar" not in st.session_state:
    st.session_state.mostrar_sidebar = False

if not st.session_state.mostrar_sidebar:
    st.set_page_config(initial_sidebar_state="collapsed")
else:
    st.set_page_config(initial_sidebar_state="expanded")

# === SESSION STATE INICIAL ===
if 'gerenciamento' not in st.session_state:
    st.session_state['gerenciamento'] = GerenciamentoPersonagens('data/entrada.txt', classes_dict, habilidades_dict)

if 'personagens_lidos' not in st.session_state:
    st.session_state['personagens_lidos'] = st.session_state.gerenciamento.get_personagens()

if 'gerenciamento_arenas' not in st.session_state:
    st.session_state['gerenciamento_arenas'] = GerenciamentoArenas('data/arenas.txt', mapas_dict, tipos_jogo)

if 'arenas_lidas' not in st.session_state:
    st.session_state['arenas_lidas'] = st.session_state['gerenciamento_arenas'].get_arenas()

if 'arena_combate' not in st.session_state:
    st.session_state['arena_combate'] = None

if 'id_partida' not in st.session_state:
    st.session_state['id_partida'] = None

# === NAVEGAÇÃO ===
pages = {
    "Pages": [
        st.Page("pages/inicial.py", title="🧙‍ Inicial"),
        st.Page("pages/personagens.py", title="🧙‍ Personagens"),
        st.Page("pages/arenas.py", title="🏟️ Arenas"),
        st.Page("pages/combate.py", title="⚔️ Combate"),
        st.Page("pages/relatorio_combate.py", title="📜 Relatório de Combate"),
    ]
}

pg = st.navigation(pages)
pg.run()
