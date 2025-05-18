from utils.page_functions.criar_personagem import criar_personagem
from utils.page_functions.galeria_personagens import criar_card_personagem
from utils.streamlit_utils import set_background_as_frame
from utils.streamlit_utils import get_image_path
from utils.streamlit_utils import exibir_logs_chat_generico
import streamlit as st
import os

mostrar, criar, logs = st.tabs(['Galeria de Personagens', 'Criar Personagem', 'Logs'])
set_background_as_frame(get_image_path('assets/images/extras/fundo.png'))
classes = list(st.session_state.gerenciamento.classes_dict.keys())
classes = ['Todos'] + classes

personagens_lidos = st.session_state.personagens_lidos
with st.sidebar:
    st.write('### 📤 Importar Personagens')
    personagens_file = st.file_uploader("Enviar arquivo de personagens (.txt)", type=["txt"], key="personagens")

    if personagens_file and not st.session_state.get("personagens_importados", False):
        st.session_state.gerenciamento.importar_adicionando_personagens(personagens_file)
        st.session_state.personagens_lidos = st.session_state.gerenciamento.get_personagens()
        st.session_state.personagens_importados = True  # evita reimportação
        st.success("Personagens importados com sucesso!")
        st.rerun()

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

with logs:
    exibir_logs_chat_generico("data/logs_personagem.txt", titulo="📜 Erro Importação de Personagens")



