import streamlit as st
from utils.page_functions.criar_personagem import criar_personagem
from utils.page_functions.galeria_personagens import criar_card_personagem
from utils.caminhos import get_image_path
from utils.logs import exibir_logs_chat_generico
from utils.visual import background
from utils.visual import set_background_as_frame


# === Plano de fundo da aplicação ===
if st.toggle('Ativar Container', True):
    set_background_as_frame(get_image_path('assets/images/extras/fundo.png'))
else:
    background(get_image_path('assets/images/extras/fundo.png'))
# === Criação das abas principais ===
mostrar, criar, logs = st.tabs(['Galeria de Personagens', 'Criar Personagem', 'Logs'])

# === Carrega classes disponíveis e adiciona opção "Todos" ===
classes = list(st.session_state.gerenciamento.classes_dict.keys())
classes = ['Todos'] + classes

# === Carrega personagens já existentes no session_state ===
personagens_lidos = st.session_state.personagens_lidos

# === Barra lateral: Upload, Filtros e Importação ===
with st.sidebar:
    st.write('### 📤 Importar Personagens')

    # Upload de arquivo de personagens
    personagens_file = st.file_uploader("Enviar arquivo de personagens (.txt)", type=["txt"], key="personagens")

    # Importa personagens uma única vez por sessão
    if personagens_file and not st.session_state.get("personagens_importados", False):
        st.session_state.gerenciamento.importar_adicionando_personagens(personagens_file)
        st.session_state.personagens_lidos = st.session_state.gerenciamento.get_personagens()
        st.session_state.personagens_importados = True  # Impede importações duplicadas
        st.success("Personagens importados com sucesso!")
        st.rerun()  # Recarrega a página para atualizar visualmente os personagens

    # Filtro por classe
    classe_selecionada = st.selectbox('Filtre por Classe', classes)
    if classe_selecionada != 'Todos':
        personagens_lidos = [
            personagem for personagem in personagens_lidos
            if personagem.classe.nome == classe_selecionada
        ]

# === Aba "Galeria de Personagens" ===
with mostrar:
    c1, c2 = st.columns([3, 1.3])

    # Exibe o total de personagens
    c1.write(f"### Personagens Criados: {len(personagens_lidos)}")

    # Botão de download do arquivo de personagens
    with open('data/personagens.txt', "rb") as f:
        c2.download_button(
            label="📥 Baixar Arquivo de Personagens",
            data=f,
            file_name='personagens.txt',
            mime="text/plain"
        )

    # Exibe os personagens em dois blocos de coluna
    cols = st.columns(2)
    for i, personagem in enumerate(personagens_lidos):
        col = cols[i % 2]  # Alterna entre coluna 0 e 1
        with col:
            criar_card_personagem(personagem)

# === Aba "Criar Personagem" ===
with criar:
    criar_personagem()

# === Aba "Logs de Personagens" ===
with logs:
    exibir_logs_chat_generico("data/logs_personagem.txt", titulo="📜 Logs de Personagens")
