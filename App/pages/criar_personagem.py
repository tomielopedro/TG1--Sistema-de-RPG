import streamlit as st
from RPG import *

def criar_personagem():

    col1, col2 = st.columns(2)

    nome = ''
    classe = ''

    with col1:
        with st.container(border=True, height=500):
            st.write('#### Crie seu personagem')

            # Entrada do nome

            entrada_nome = st.text_input('Nome:', max_chars=15, placeholder='Insira o nome do personagem')
            entrada_nome = entrada_nome.strip().capitalize()
            if entrada_nome != '':
                if not st.session_state.gerenciamento.verifica_existencia(entrada_nome):
                    nome = entrada_nome
                else:
                    st.warning('Já existe um personagem com esse nome!')
            else:
                st.warning('É obrigatório criar um nome para o personagem')

            # Seleção da classe
            classe_nome = st.selectbox('Classe', list(st.session_state.gerenciamento.classes_dict.keys()))
            classe = st.session_state.gerenciamento.classes_dict.get(classe_nome)

            # Seleção das habilidades com base na classe escolhida
            if classe is not None:
                limite = classe.limite_habilidades
                with st.container(border=True, height=300):
                    st.write(f'##### Selecione até {limite} habilidades')

                    habilidades_selecionadas = []
                    for c in range(limite):
                        habilidade_nome = st.selectbox(
                            f'Habilidade {c + 1} de {limite}:',
                            list(st.session_state.gerenciamento.habilidades_dict.keys()),
                            key=f'Habilidade_{c}'
                        )
                        habilidades_selecionadas.append(st.session_state.gerenciamento.habilidades_dict.get(habilidade_nome))
                    habilidades = habilidades_selecionadas

    # Botões de ação
    c1, c2 = st.columns(2)
    liberado = nome != '' and classe is not None and len(habilidades) > 0
    with c1:
        criar_personagem = st.button('Criar Personagem', disabled=not liberado)

    # Verifica se deve criar personagem
    with c2:
        if criar_personagem:
            st.session_state.gerenciamento.salvar_personagem(nome, classe, habilidades)
            st.success('✅ Personagem criado com sucesso!')
            st.balloons()

    # COLUNA 2 - Pré-visualização

    with col2:
        with st.container(border=True, height=500):
            st.write('#### Pré-Visualização')

            if classe:
                img_col, info_col = st.columns([1, 3])

                # Mostra imagem do personagem
                with img_col:
                    st.image(classe.foto, width=100)

                # Informações básicas
                with info_col:
                    st.write(f'#### {nome} - {classe.nome}')

                # Atributos do personagem
                st.write(f'###### 🔋 :green[Vida:] {classe.pontos_vida}')
                st.write(f'###### ⚔️ :red[Ataque:] {classe.pontos_ataque}')
                st.write(f'###### 🛡️ :blue[Defesa:] {classe.pontos_defesa}')
                st.write(f':gray[Dado de Ataque:] {classe.dado_ataque} | '
                         f':gray[Limite de Habilidades:] {classe.limite_habilidades}')

                # Habilidades escolhidas
                # Habilidades escolhidas
                cols = st.columns(5)
                for i, habilidade in enumerate(habilidades):
                    col = cols[i % 5]
                    col.image(habilidade.foto_habilidade, width=100)
            else:
                st.info("Selecione uma classe para visualizar o personagem.")


