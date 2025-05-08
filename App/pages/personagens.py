from RPG import *  # Importa classes como Mago, Guerreiro, Personagem, habilidades, etc.
from utils import GerenciamentoPersonagens  # Gerenciador de leitura/escrita de personagens
import streamlit as st
import streamlit.components.v1 as components

# Dados disponíveis para lançamento
dados = [D4(), D6(), D8(), D10(), D12(), D20()]


# Função para lançar dado com animação CSS
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

    # Renderiza dado animado na interface
    components.html(html_code, height=200)
    return numero


# Sidebar do app
with st.sidebar:
    st.title('Sistema de RPG')
    st.divider()


# Título principal da página com contador de personagens
st.title(f"Personagens Criados: {Personagem.personagens_criados}")
st.divider()
# Cria duas colunas para exibir personagens lado a lado
cols = st.columns(2)
personagens_mortos = []
# Itera sobre os personagens lidos
for i, personagem in enumerate(st.session_state.personagens_lidos):
    col = cols[i % 2]  # Alterna entre coluna 0 e 1
    nome = f'#### {personagem.nome} - {personagem.classe.nome}'
    disabled = False
    if personagem.pontos_vida <= 0:
        nome = f'#### ~~{personagem.nome} - {personagem.classe.nome}~~'
        personagens_mortos.append(personagem)
        disabled = True

        st.write(f'#### {personagem.nome} - {personagem.classe.nome}')
    with col.container(border=True):
        # Layout interno com imagem e informações
        img_col, info_col = st.columns([1, 3])

        with img_col:
            # Mostra a imagem da classe
            st.image(personagem.classe.foto, width=100)

        with info_col:

            st.write(f'{nome}')

        # Atributos do personagem
        st.write(f'###### 🔋 :green[Vida:] {personagem.pontos_vida}')
        st.write(f'###### ⚔️ :red[Ataque:] {personagem.pontos_ataque}')
        st.write(f'###### 🛡️ :blue[Defesa:] {personagem.pontos_defesa}')
        st.write(
            f':gray[Dado de Ataque:] {personagem.dado_ataque} | :gray[Limite de Habilidades:] {personagem.classe.limite_habilidades}')

        # Seleção de habilidade e alvo
        col_select1, col_select2 = st.columns(2)

        with col_select1:
            # Seleciona uma habilidade do inventário
            habilidade = st.selectbox(
                'Habilidades: ',
                personagem.inventario,
                key=f'SelecionarHabilidade-{personagem.nome}',
                format_func=lambda x: x.__repr__(), disabled=disabled  # Mostra o nome da habilidade
            )

        with col_select2:
            st.number_input('Pontos de Habilidade', habilidade.pontos_ataque,  key=f'PontosHabilidade-{personagem.nome}', disabled=disabled )


            # Filtra alvos (outros personagens)
        alvos_disponiveis = [p for p in st.session_state.personagens_lidos if p != personagem and p not in personagens_mortos]
        alvo = st.selectbox(
            'Alvo: ',
            alvos_disponiveis,
            key=f'SelecionarAlvo-{personagem.nome}',
            format_func=lambda x: x.__repr__(),
            disabled=disabled
        )

        # Botão de ataque
        if st.button('⚔️ Atacar ⚔️', key=f'AtacarAlvo-{personagem.nome}', disabled=disabled):
            numero = lancar_dado(personagem.classe.dado_ataque)
            dano, usou_habilidade = personagem.atacar(alvo, habilidade)
            dano*=numero

            if usou_habilidade:
                st.warning(
                    f'{personagem.nome} atacou {alvo.nome} com {habilidade.nome} causando {personagem.pontos_ataque} * {numero} = {dano} de dano')
                st.balloons()
            else:
                st.warning(
                    f'{personagem.nome} atacou {alvo.nome} sem habilidade causando {personagem.pontos_ataque} * {numero} = {dano} de dano')
                st.snow()
            for idx, p in enumerate(st.session_state.personagens_lidos):
                if p.nome == alvo.nome:
                    st.session_state.personagens_lidos[idx] = alvo  # Reatribui com valor modificado
                    break
            # Efeito visual

