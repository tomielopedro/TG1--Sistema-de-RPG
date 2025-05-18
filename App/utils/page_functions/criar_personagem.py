import streamlit as st
from RPG import *


def exibir_formulario_criacao(col):
    """
    Exibe o formulário de criação do personagem (nome, classe, habilidades).
    Retorna nome, classe e habilidades selecionadas.
    """
    nome, classe, habilidades = '', None, []

    with col:
        with st.container(border=True, height=500):
            st.write('#### Crie seu personagem')

            # Entrada do nome
            entrada_nome = st.text_input('Nome:', max_chars=15, placeholder='Insira o nome do personagem')
            entrada_nome = entrada_nome.strip().capitalize()

            if entrada_nome:
                if not st.session_state.gerenciamento.verifica_existencia(entrada_nome):
                    nome = entrada_nome
                else:
                    st.warning('Já existe um personagem com esse nome!')
            else:
                st.warning('É obrigatório criar um nome para o personagem')

            # Seleção da classe
            classe_nome = st.selectbox('Classe', list(st.session_state.gerenciamento.classes_dict.keys()))
            classe = st.session_state.gerenciamento.classes_dict.get(classe_nome)

            # Seleção das habilidades
            if classe:
                limite = classe.limite_habilidades
                with st.container(border=True, height=300):
                    st.write(f'##### Selecione até {limite} habilidades')

                    for i in range(limite):
                        habilidade_nome = st.selectbox(
                            f'Habilidade {i + 1} de {limite}:',
                            list(st.session_state.gerenciamento.habilidades_dict.keys()),
                            key=f'Habilidade_{i}'
                        )
                        habilidade = st.session_state.gerenciamento.habilidades_dict.get(habilidade_nome)
                        habilidades.append(habilidade)

    return nome, classe, habilidades


def exibir_pre_visualizacao(col, nome, classe, habilidades):
    """
    Exibe a pré-visualização do personagem com seus atributos e habilidades.
    """
    with col:
        with st.container(border=True, height=500):
            st.write('#### Pré-Visualização')

            if classe:
                img_col, info_col = st.columns([1, 3])

                with img_col:
                    st.image(classe.foto, width=100)

                with info_col:
                    st.write(f'#### {nome} - {classe.nome}')

                st.write(f'###### 🔋 :green[Vida:] {classe.pontos_vida}')
                st.write(f'###### ⚔️ :red[Ataque:] {classe.pontos_ataque}')
                st.write(f'###### 🛡️ :blue[Defesa:] {classe.pontos_defesa}')
                st.write(f':gray[Dado de Ataque:] {classe.dado_ataque} | '
                         f':gray[Limite de Habilidades:] {classe.limite_habilidades}')

                cols = st.columns(5)
                for i, habilidade in enumerate(habilidades):
                    cols[i % 5].image(habilidade.foto_habilidade, width=100)
            else:
                st.info("Selecione uma classe para visualizar o personagem.")


def criar_personagem():
    """
    Função principal que organiza a interface de criação do personagem.
    """
    col1, col2 = st.columns(2)

    # === Formulário de criação ===
    nome, classe, habilidades = exibir_formulario_criacao(col1)

    # === Botões de ação ===
    c1, c2 = st.columns(2)
    pode_criar = nome != '' and classe is not None and len(habilidades) > 0

    with c1:
        criar = st.button('Criar Personagem', disabled=not pode_criar)

    with c2:
        if criar:
            st.session_state.gerenciamento.salvar_personagem(nome, classe, habilidades)
            st.success('✅ Personagem criado com sucesso!')
            st.balloons()

    # === Pré-visualização do personagem ===
    exibir_pre_visualizacao(col2, nome, classe, habilidades)
