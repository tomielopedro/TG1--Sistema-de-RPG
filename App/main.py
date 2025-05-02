from RPG import *
from utils import HandlePersonagens
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(layout="wide")

st.title("Arena 1")
st.divider()

dados = [D4(), D6(), D8(), D10(), D12(), D20(),]


def lancar_dado(dado):

    numero = dado.jogar()
    html_code = f"""
    <style>
    .dado {{
      width: 120px;
      height: 120px;
      border-radius: 10px;
      background: white;
      color: black;
      font-size: 48px;
      font-weight: bold;
      display: flex;
      justify-content: center;
      align-items: center;
      animation: girar 0.6s ease;
      margin: 20px auto;
      border: 3px solid #333;
    }}
    
    @keyframes girar {{
      0%   {{ transform: rotateY(0deg); }}
      50%  {{ transform: rotateY(180deg); }}
      100% {{ transform: rotateY(360deg); }}
    }}
    </style>
    
    <div class="dado">{numero}</div>
    
"""

    components.html(html_code, height=200)
    return numero

with st.sidebar:
    st.title('Sistema de RPG')
    st.divider()
classes = {
    'Mago': Mago(),
    'Guerreiro': Guerreiro(),
    'Ladino': Ladino()
}

habilidades_permitidas = {
    'BolaDeFogo': BolaDeFogo(),
    'Cura': Cura(),
    'Tiro de Arco': TiroDeArco()
}

handle_personagens = HandlePersonagens('data/entrada.txt', classes, habilidades_permitidas)
personagens_lidos = handle_personagens.ler_personagens()

cols = st.columns(2)

for i, personagem in enumerate(personagens_lidos):
    col = cols[i % 2]
    with col.container(border=True):
        img_col, info_col = st.columns([1, 3])

        with img_col:
            st.image(personagem.classe.foto, width=100)

        with info_col:
            st.write(f'#### {personagem.nome} - {personagem.classe.nome}')

        st.write(f'###### 🔋 :green[Vida:] {personagem.classe.pontos_vida}')
        st.write(f'###### ⚔️ :red[Ataque:] {personagem.classe.pontos_ataque}')
        st.write(f'###### 🛡️ :blue[Defesa:] {personagem.classe.pontos_defesa}')
        st.write(f':gray[Dado de Ataque:] {personagem.classe.dado_ataque} | :gray[Limite de Habilidades:] {personagem.classe.limite_habilidades}')
        col_select1, colselect2 = st.columns(2)
        with col_select1:
            habilidade = st.selectbox('Habilidades: ', personagem.inventario, key=f'SelecionarHabilidade-{personagem.nome}', format_func=lambda x: x.__repr__())
        with colselect2:
            alvos_disponiveis = [p for p in personagens_lidos if p != personagem]
            alvo = st.selectbox('Alvo: ', alvos_disponiveis, key=f'SelecionarAlvo-{personagem.nome}', format_func=lambda x: x.__repr__())
        if st.button('⚔️ Atacar ⚔️', key=f'AtacarAlvo-{personagem.nome}'):
            numero = lancar_dado(personagem.classe.dado_ataque)
            st.warning(f'{personagem.nome} atacou {alvo.nome} com {habilidade.nome} causando {personagem.pontos_ataque} * {numero} = {personagem.pontos_ataque*numero} de dano')
            st.balloons()



