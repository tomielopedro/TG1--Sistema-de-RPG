from RPG import *
from utils.streamlit_utils import modal_card_personagem
import streamlit as st


def criar_arena():

    col1, col2 = st.columns(2)
    with col1:
        with st.container(height=450, border=True):
            st.write('##### Crie sua arena')
            nome_arena = st.text_input('Insira o nome do arena', max_chars=10)
            mapa = st.selectbox('Selecione o mapa da arena', st.session_state.gerenciamento_arenas.mapas_dict.keys())
            mapa = st.session_state.gerenciamento_arenas.mapas_dict.get(mapa)
            tipo_arena = st.selectbox('Selecione o tipo de arena', st.session_state.gerenciamento_arenas.tipo_dict.keys())
            tipo_arena = st.session_state.gerenciamento_arenas.tipo_dict.get(tipo_arena)
            # Checkbox apenas se for PVP
            select_todos = False
            if tipo_arena.nome == 'PVP':
                select_todos = st.checkbox('Selecionar todos os jogadores')

            # Determina os personagens a mostrar e os pré-selecionados
            personagens_disponiveis = st.session_state.personagens_lidos
            default_selecionados = personagens_disponiveis if select_todos else []

            # Garante que não ultrapasse o limite
            default_selecionados = default_selecionados[:tipo_arena.limite_jogadores]

            # Multiselect
            personagens_arena = st.multiselect(
                'Selecione os Jogadores:',
                personagens_disponiveis,
                default=default_selecionados,
                max_selections=tipo_arena.limite_jogadores,
                format_func=lambda x: x.__repr__()
            )

    with col2:
        with st.container(height=450, border=True):
            st.write('##### Pré Visualização')
            c1, c2 = st.columns([1, 3])
            with c1:
                st.image(tipo_arena.icone, width=100)
            with c2:
                st.write(f'#### {nome_arena} - {tipo_arena.nome}')
            st.write(f':gray[Limite de jogadores:] {tipo_arena.limite_jogadores}')
            st.image(mapa.foto_mapa, use_container_width=True)
            personagem = st.pills("Personagens na Arena:",
                                  personagens_arena,
                                  format_func=lambda x: x.__repr__(),
                                  key=nome_arena)
            if personagem:
                modal_card_personagem(personagem)

    if col1.button('Criar Arena'):
        st.session_state.gerenciamento_arenas.salvar_arena(nome_arena, tipo_arena, mapa, personagens_arena)
        col2.success('✅ Arena criado com sucesso!')
        st.balloons()







