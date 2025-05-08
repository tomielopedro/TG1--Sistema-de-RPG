import streamlit as st

# Configurações iniciais
st.set_page_config(layout='wide')


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
