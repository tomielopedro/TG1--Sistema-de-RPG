import streamlit as st

from RPG import *  # Importa classes como Mago, Guerreiro, Personagem, habilidades, etc.
from utils import GerenciamentoPersonagens
from utils import GerenciamentoArenas
from utils import streamlit_utils
import streamlit.components.v1 as components

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
    'Winter': Winter(),
    'Castle': Castle(),
}

tipos_jogo = {
    'X1': X1(),
    'PVP': PVP()
}


if 'gerenciamento' not in st.session_state:
    st.session_state['gerenciamento'] = GerenciamentoPersonagens('data/entrada.txt', classes_dict, habilidades_dict)

if 'personagens_lidos' not in st.session_state:
    st.session_state['personagens_lidos'] = st.session_state.gerenciamento.get_personagens()

if 'gerenciamento_arenas' not in st.session_state:
    st.session_state['gerenciamento_arenas'] = GerenciamentoArenas('data/arenas.txt', mapas_dict, tipos_jogo)

if 'arenas_lidas' not in st.session_state:
    st.session_state['arenas_lidas'] = st.session_state.gerenciamento_arenas.get_arenas()

if 'arena_combate' not in st.session_state:
    st.session_state['arena_combate'] = None

pages = {
    "Pages": [
        st.Page("pages/personagens.py", title="Personagens"),
        st.Page("pages/arenas.py", title="Arenas"),
        st.Page("pages/combate.py", title="Combate"),
        st.Page("pages/teste.py", title="Teste"),

    ],
    "Configurações": [
    ],
}

pg = st.navigation(pages)
pg.run()
