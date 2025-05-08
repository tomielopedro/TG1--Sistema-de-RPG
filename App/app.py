import streamlit as st
from RPG import *  # Importa classes como Mago, Guerreiro, Personagem, habilidades, etc.
from utils import GerenciamentoPersonagens

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
# Configurações iniciais
st.set_page_config(layout='wide')
if 'gerenciamento' not in st.session_state:
    st.session_state['gerenciamento'] = GerenciamentoPersonagens('data/entrada.txt', classes_dict, habilidades_dict)

if 'personagens_lidos' not in st.session_state:
    st.session_state['personagens_lidos'] = st.session_state.gerenciamento.get_personagens()


pages = {
    "Dashboard": [
        st.Page("pages/personagens.py", title="Personagens"),

    ],
    "Configurações": [
        st.Page("pages/criar_personagem.py", title="Criar Personagem"),
    ],
}

pg = st.navigation(pages)
pg.run()
