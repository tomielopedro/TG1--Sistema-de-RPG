import streamlit as st
from streamlit_extras.tags import tagger_component
import os
from PIL import Image
from RPG import *

def exportar_arenas_para_txt(arenas: List['Arena'], caminho: str = "data/historico_arenas.txt"):
    with open(caminho, "a", encoding="utf-8") as f:
        for arena in arenas:
            f.write(f"=== Arena: {arena.nome_arena} ===\n")
            f.write(f"Tipo: {arena.tipo_jogo} | Mapa: {arena.mapa}\n\n")

            for partida in arena.partidas:
                f.write(f"--- Partida {partida.id}: {partida.descricao} ---\n")
                for log in partida.logs:
                    f.write(f"[Log] {log.atacante} ({log.atacante_classe}) atacou {log.alvo} ({log.alvo_classe})\n")
                    f.write(f"  D20: {log.numero_d20} | Dano Total: {log.ataque_total} | "
                            f"Defesa do Alvo: {log.alvo_pontos_defesa} | "
                            f"Habilidade: {log.habilidade_ataque} | "
                            f"Vida do Alvo após ataque: {log.alvo_vida}\n")
                f.write("\n")
            f.write("\n")

def criar_card_personagem(personagem):

    with st.container(border=True, height=400):
        img_col, info_col, ajustes_col = st.columns([1, 3, 0.5])

        # Mostra imagem do personagem
        with img_col:
            st.image(personagem.classe.foto, width=100)

        # Informações básicas
        with info_col:
            st.write(f'#### {personagem.nome} - {personagem.classe.nome}')

        # Atributos do personagem
        st.write(f'###### 🔋 :green[Vida:] {personagem.pontos_vida}')
        st.write(f'###### ⚔️ :red[Ataque:] {personagem.classe.pontos_ataque}')
        st.write(f'###### 🛡️ :blue[Defesa:] {personagem.pontos_defesa}')
        st.write(f':gray[Dado de Ataque:] {personagem.dado_ataque} | '
                 f':gray[Limite de Habilidades:] {personagem.classe.limite_habilidades}')

        if ajustes_col.button('⚙️', key=f'personagem_{personagem.nome}'):
            st.balloons()

        # Habilidades escolhidas
        if personagem.inventario:
            st.pills("Hablidades:", personagem.inventario, format_func=lambda x: x.__repr__(), key=f'Pills_{personagem.nome}')
@st.dialog('Visualização de personagem: ')
def modal_card_personagem(personagem):
    criar_card_personagem(personagem)

@st.dialog('Editar Arena')
def modal_editar_arene(arena):
    # Nome da arena
    nome_arena = st.text_input('Nome da Arena', value=arena.nome_arena, max_chars=10)

    # === Mapa da arena ===
    mapas_dict = st.session_state.gerenciamento_arenas.mapas_dict
    chaves_mapas = list(mapas_dict.keys())

    # Encontrar a chave correspondente ao valor atual de arena.maps
    chave_mapa_atual = next((k for k, v in mapas_dict.items() if k == arena.mapa), chaves_mapas[0])

    # Selectbox para mapa
    mapa_chave = st.selectbox(
        'Mapa da arena',
        chaves_mapas,
        index=chaves_mapas.index(chave_mapa_atual),
        key=f'EditarMapa{arena.nome_arena}'

    )
    mapa = mapas_dict[mapa_chave]

    # === Tipo da arena ===
    tipos_dict = st.session_state.gerenciamento_arenas.tipo_dict
    chaves_tipos = list(tipos_dict.keys())

    # Encontrar a chave correspondente ao tipo atual
    chave_tipo_atual = next((k for k, v in tipos_dict.items() if k == arena.tipo_jogo), chaves_tipos[0])

    # Selectbox para tipo
    tipo_chave = st.selectbox(
        'Selecione o tipo de arena',
        chaves_tipos,
        index=chaves_tipos.index(chave_tipo_atual),
        key=f'EditarTipo{arena.nome_arena}'
    )
    tipo_arena = tipos_dict[tipo_chave]

    # === Seleção de jogadores ===
    select_todos = False
    if tipo_arena.nome == 'PVP':
        select_todos = st.checkbox('Selecionar todos os jogadores')

    personagens_disponiveis = st.session_state.personagens_lidos
    default_selecionados = personagens_disponiveis if select_todos else arena.lista_personagens

    # Limitar os personagens selecionados ao máximo permitido
    default_selecionados = default_selecionados[:tipo_arena.limite_jogadores]

    # Multiselect de jogadores
    personagens_arena = st.multiselect(
        'Selecione os Jogadores:',
        personagens_disponiveis,
        default=default_selecionados,
        max_selections=tipo_arena.limite_jogadores,
        format_func=lambda x: x.__repr__(),
        key=f'EditarJogadores{arena.nome_arena}'
    )
    c1, c2, c3 = st.columns([1, 1, 2])
    if c1.button('📥 Salvar '):
        st.session_state.gerenciamento_arenas.editar_arena(arena, nome_arena, tipo_arena, mapa, personagens_arena)
        st.rerun()

    if c2.button('🗑️ Excluir '):
        st.session_state.gerenciamento_arenas.excluir_arena(arena)
        st.rerun()

def criar_card_arena(arena):

    with st.container(height=400, border=True):
        c1, c2,c3 = st.columns([1, 3, 0.5])
        with c1:
            st.image(arena.icone, width=100)
        with c2:
            st.write(f'#### {arena.nome_arena} - {arena.tipo_jogo}')


        st.write(f':gray[Jogadores:] {len(arena.lista_personagens)} | :gray[Limite:] {arena.limite_jogadores}')
        st.image(arena.foto_mapa, use_container_width=True)
        if arena.lista_personagens:
            personagem = st.pills("Personagens na Arena:",
                                  arena.lista_personagens,
                                  format_func=lambda x: x.__repr__(),
                                  key=arena.nome_arena)
            if personagem:
                modal_card_personagem(personagem)

        if c3.button('⚙️', key=f'ajuste_{arena.nome_arena}'):
            modal_editar_arene(arena)

    if st.button('🚪 Entrar na arena', key=f'Combate_{arena.nome_arena}', use_container_width=True, type='primary'):
        st.session_state.arena_combate = arena
        st.switch_page("pages/combate.py")



