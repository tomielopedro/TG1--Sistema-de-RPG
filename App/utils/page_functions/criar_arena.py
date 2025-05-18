import streamlit as st
from RPG import *
from utils.page_functions.galeria_personagens import modal_card_personagem
from utils.page_functions.galeria_personagens import modal_card_personagem
from utils.streamlit_utils import get_image_path

def exibir_formulario_criacao_arena():
    """
    Exibe o formulário de criação da arena, com validações de nome e retorno dos dados preenchidos.
    """
    with st.container(height=450, border=True):
        st.write('##### Crie sua arena')

        nome_validado = ''
        nome_arena = st.text_input('Insira o nome da arena', max_chars=15, placeholder='Nome da arena').strip().capitalize()

        # Verificação de nome preenchido e duplicado
        if nome_arena:
            if not st.session_state.gerenciamento_arenas.verifica_existencia(nome_arena):
                nome_validado = nome_arena
            else:
                st.warning('⚠️ Já existe uma arena com esse nome!')
        else:
            st.warning('⚠️ É obrigatório inserir um nome para a arena.')

        # Seleção do mapa
        mapa_nome = st.selectbox('Selecione o mapa da arena', st.session_state.gerenciamento_arenas.mapas_dict.keys())
        mapa = st.session_state.gerenciamento_arenas.mapas_dict.get(mapa_nome)

        # Seleção do tipo
        tipo_nome = st.selectbox('Selecione o tipo de arena', st.session_state.gerenciamento_arenas.tipo_dict.keys())
        tipo_arena = st.session_state.gerenciamento_arenas.tipo_dict.get(tipo_nome)

        # Seleção de personagens
        select_todos = tipo_arena.nome == 'PVP' and st.checkbox('Selecionar todos os jogadores')

        personagens_disponiveis = st.session_state.personagens_lidos
        default_selecionados = personagens_disponiveis if select_todos else []
        default_selecionados = default_selecionados[:tipo_arena.limite_jogadores]

        personagens_arena = st.multiselect(
            'Selecione os Jogadores:',
            personagens_disponiveis,
            default=default_selecionados,
            max_selections=tipo_arena.limite_jogadores,
            format_func=lambda x: x.__repr__()
        )
        if len(personagens_arena)<2:
            st.warning('Selecione no mínimo dois personagens')

        return nome_validado, mapa, tipo_arena, personagens_arena


def exibir_pre_visualizacao_arena(nome_arena, mapa, tipo_arena, personagens_arena):
    """
    Mostra uma pré-visualização da arena antes de sua criação.
    """
    with st.container(height=450, border=True):
        st.write('##### Pré Visualização')

        c1, c2 = st.columns([1, 3])
        with c1:
            st.image(get_image_path(tipo_arena.icone), width=100)
        with c2:
            st.write(f'#### {nome_arena} - {tipo_arena.nome}')

        st.write(f':gray[Limite de jogadores:] {tipo_arena.limite_jogadores}')
        st.image(mapa.icone_mapa, use_container_width=True)

        personagem = st.pills(
            "Personagens na Arena:",
            personagens_arena,
            format_func=lambda x: x.__repr__(),
            key=nome_arena
        )

        if personagem:
            modal_card_personagem(personagem)


def criar_arena():
    """
    Interface para criar uma arena. Realiza validações e organiza entrada, pré-visualização e salvamento.
    """
    col1, col2 = st.columns(2)

    with col1:
        nome_arena, mapa, tipo_arena, personagens_arena = exibir_formulario_criacao_arena()

    with col2:

        exibir_pre_visualizacao_arena(nome_arena, mapa, tipo_arena, personagens_arena)
    disabled = (not nome_arena) or (len(personagens_arena) < 2)
    if col1.button('Criar Arena', disabled=disabled):


        # Salvar arena
        st.session_state.gerenciamento_arenas.salvar_arena(nome_arena, tipo_arena, mapa, personagens_arena)
        col2.success('✅ Arena criada com sucesso!')
        st.balloons()

