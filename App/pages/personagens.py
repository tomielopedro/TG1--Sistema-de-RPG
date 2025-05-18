from utils.page_functions.criar_personagem import criar_personagem
from utils.page_functions.galeria_personagens import criar_card_personagem
from utils.streamlit_utils import set_background_as_frame
import streamlit as st



mostrar, criar= st.tabs(['Galeria de Personagens', 'Criar Personagem'])
set_background_as_frame('./assets/images/extras/fundo.png')
classes = list(st.session_state.gerenciamento.classes_dict.keys())
classes = ['Todos'] + classes

personagens_lidos = st.session_state.personagens_lidos
with st.sidebar:

    classe_selecionada = st.selectbox('Filtre por Classe', classes)
    if classe_selecionada != 'Todos':
        personagens_lidos = [personagem for personagem in personagens_lidos if personagem.classe.nome == classe_selecionada]


with mostrar:
    st.write(f"### Personagens Criados: {len(personagens_lidos)}")
    cols = st.columns(2)
    # Itera sobre os personagens lidos
    for i, personagem in enumerate(personagens_lidos):
        col = cols[i % 2]  # Alterna entre coluna 0 e 1
        with col:
            criar_card_personagem(personagem)
with criar:
    criar_personagem()


