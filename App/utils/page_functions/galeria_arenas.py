import streamlit as st
import pandas as pd
from streamlit_avatar import avatar
from utils.logs import converter_logs_em_df
from utils.caminhos import get_image_base64
from utils.caminhos import get_image_path
from utils.page_functions.galeria_personagens import modal_card_personagem



def resetar_estado_combate():
    """
    Remove variáveis de estado do combate no Streamlit e reinstancia os personagens
    para nova batalha sem perder os dados de origem.
    """
    if st.session_state.arena_combate is not None:
        for chave in ["personagens_vivos", "personagens_mortos", "logs_visuais", "turno", "fila_turno"]:
            st.session_state.pop(chave, None)

        personagens_novos = [
            p.__copy__() for p in st.session_state.personagens_lidos
            if p in st.session_state.arena_combate.lista_personagens
        ]
        st.session_state.arena_combate.lista_personagens = personagens_novos


def get_ids_partidas_arena(df: pd.DataFrame, nome_arena: str):

    if 'arena' not in df.columns or 'id_partida' not in df.columns:
        raise ValueError("O DataFrame precisa conter as colunas 'arena' e 'id_partida'.")

    partidas_vencidas = df[df['arena'] == nome_arena]
    return partidas_vencidas['id_partida'].tolist()


def exibir_estatisticas_arena(historico_df: pd.DataFrame, nome_arena: str, st_container=st):

    sc = st_container
    df_arena = historico_df[historico_df['arena'] == nome_arena]

    if df_arena.empty:
        sc.warning("Nenhuma partida realizada nessa arena")
        return

    total_partidas = len(df_arena)

    # === Personagem com mais vitórias ===
    contagem_vitorias = df_arena['vencedor'].value_counts()
    vencedor_nome = contagem_vitorias.idxmax()
    qtd_vitorias_top = contagem_vitorias.max()

    # === Logs da arena ===
    logs_df = converter_logs_em_df(df_arena['logs'].tolist())

    # === Mapeia classes vencedoras ===
    vencedores = df_arena['vencedor'].tolist()

    logs_vencedores = logs_df[
        (logs_df['alvo'].isin(vencedores)) &
        (logs_df['alvo_vida'] > 0)
        ][['alvo', 'alvo_classe']].drop_duplicates()

    # Conta quantas vezes cada classe venceu
    contagem_classes = logs_vencedores['alvo_classe'].value_counts()
    taxa_por_classe = (contagem_classes / total_partidas * 100).reset_index()
    taxa_por_classe.columns = ['classe', 'porcentagem_vitorias']

    # === Exibição ===
    sc.markdown(f"### 🏟️ Estatísticas da Arena: `{nome_arena}`")
    sc.write(f"**Total de Partidas:** {total_partidas}")
    vencedor = next((p for p in st.session_state.personagens_lidos if p.nome == vencedor_nome), None)

    if vencedor:
        st.write(f"**Maior Vencedor:**")
        avatar([{ "url": f"data:image/png;base64,{get_image_base64(vencedor.classe.foto)}", "size": 100, "title": vencedor.nome, "caption": f"👑 {vencedor.classe.nome} Vitórias: {qtd_vitorias_top}", "key": f"arena{nome_arena}" }])
    sc.markdown("---")


@st.dialog('Editar Arena')
def modal_editar_arene(arena):
    # Nome da arena
    nome_arena = st.text_input('Nome da Arena', value=arena.nome_arena, max_chars=10)

    # === Mapa da arena ===
    mapas_dict = st.session_state.gerenciamento_arenas.mapas_dict
    chaves_mapas = list(mapas_dict.keys())

    # Encontrar a chave correspondente ao valor atual de arena.mapas
    chave_mapa_atual = next((k for k, v in mapas_dict.items() if k == arena.mapa.nome_mapa), chaves_mapas[0])

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
        informacoes, estatisticas, partidas = st.tabs(['Informações', 'Estatísticas', 'Partidas'])
        with informacoes:
            c1, c2,c3 = st.columns([1, 3, 0.5])
            with c1:
                st.image(get_image_path(arena.icone), width=100)
            with c2:
                st.write(f'#### {arena.nome_arena} - {arena.tipo_jogo}')


            st.write(f':gray[Jogadores:] {len(arena.lista_personagens)} | :gray[Limite:] {arena.limite_jogadores}')
            st.image(arena.mapa.icone_mapa, use_container_width=True)
            if arena.lista_personagens:
                personagem = st.pills("Personagens na Arena:",
                                      arena.lista_personagens,
                                      format_func=lambda x: x.__repr__(),
                                      key=arena.nome_arena)
                if personagem:
                    modal_card_personagem(personagem)

            if c3.button('⚙️', key=f'ajuste_{arena.nome_arena}'):
                modal_editar_arene(arena)
        df = pd.read_csv('data/historico_batalhas.csv')

        with estatisticas:
            exibir_estatisticas_arena(df, arena.nome_arena)
        with partidas:

            partidas_realizadas = get_ids_partidas_arena(df, arena.nome_arena)
            if partidas_realizadas:
                partida = st.pills('Selecione uma partida', partidas_realizadas, key=f'{arena.nome_arena}_{partidas_realizadas}')
                if partida:
                    st.session_state.id_partida = partida
                    st.switch_page('pages/relatorio_combate.py')
            else:
                st.warning('Nenhuma partida realizada nessa arena')

    disabled = len(arena.lista_personagens) <= 0
    if st.button('🚪 Entrar na arena', key=f'Combate_{arena.nome_arena}', use_container_width=True, type='primary', disabled=disabled):
        resetar_estado_combate()
        st.session_state.arena_combate = arena
        st.session_state.arena_combate.lista_personagens = [p.__copy__() for p in st.session_state.arena_combate.lista_personagens]
        st.switch_page("pages/combate.py")
