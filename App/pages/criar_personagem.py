import streamlit as st
from RPG import *
from utils import GerenciamentoPersonagens

st.title('Criar Personagens')
st.divider()

classes = {
    'Mago': Mago(),
    'Guerreiro': Guerreiro(),
    'Ladino': Ladino()
}

habilidades_permitidas = {
    'Bola De Fogo': BolaDeFogo(),
    'Cura': Cura(),
    'Tiro de Arco': TiroDeArco()
}

col1, col2 = st.columns(2)
personagem = {
    'nome': '',
    'classe': '',
    'habilidades': [],
}
handle_personagens = GerenciamentoPersonagens('data/entrada.txt', classes, habilidades_permitidas)
with (col1):
    with st.container(border=True, height=500):
        st.write('#### Crie seu personagem')
        personagem['nome'] = st.text_input('Nome:', max_chars=15, placeholder='Insira o nome do personagem')

        classe = st.selectbox('Classe', classes.keys())
        personagem['classe'] = classes.get(classe)
        with st.container(border=True, height=300):
            st.write('##### Selecione suas habilidades')
            for c in range(personagem['classe'].limite_habilidades):
                habilidade = st.selectbox(f'Habilidade {c+1}:', habilidades_permitidas.keys(), key=f'Habilidades_{c}')
                habilidade = habilidades_permitidas.get(habilidade)

                personagem['habilidades'].append(habilidade)
c1,c2 = st.columns(2)
with c1:
    criar_personagem = st.button('Criar Personagem')
with c2:
    if criar_personagem:

        if personagem['nome'] is not '' and personagem['classe'] is not '':
            handle_personagens.criar_personagens(personagem)
            st.success('Personagem criado com sucesso!')
            st.balloons()
        else:
            st.warning('Erro ao criar o personagem')


with col2:
    with st.container(border=True, height=500):
        st.write('#### Pré-Visualização')
        img_col, info_col = st.columns([1, 3])

        with img_col:
            st.image(personagem['classe'].foto, width=100)

        with info_col:
            st.write(f'#### {personagem['nome']} - {personagem['classe'].nome}')

        st.write(f'###### 🔋 :green[Vida:] {personagem['classe'].pontos_vida}')
        st.write(f'###### ⚔️ :red[Ataque:] {personagem['classe'].pontos_ataque}')
        st.write(f'###### 🛡️ :blue[Defesa:] {personagem['classe'].pontos_defesa}')
        st.write(f':gray[Dado de Ataque:] {personagem['classe'].dado_ataque} | :gray[Limite de Habilidades:] {personagem['classe'].limite_habilidades}')
        col_select1, colselect2 = st.columns(2)

        if len(personagem['habilidades']) > 0:
            st.pills("Hablidades", personagem['habilidades'], format_func=lambda x: x.__repr__())