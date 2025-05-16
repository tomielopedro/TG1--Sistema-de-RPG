from pages.criar_personagem import criar_personagem
from pages.mostrar_personagem import mostrar_personagem
import streamlit as st

mostrar, criar, teste = st.tabs(['Galeria de Personagens', 'Criar Personagem', 'Teste'])

with mostrar:
    st.write(f"### Personagens Criados: {len(st.session_state.personagens_lidos)}")
    mostrar_personagem()
with criar:
    criar_personagem()
with teste:
    st.write('Pagina de teste')

