import streamlit as st
import pandas as pd
import json
from utils.streamlit_utils import converter_logs_em_df, get_image_base64
from streamlit_avatar import avatar

# =====================================
# === Funções de Processamento de Dados
# =====================================

def get_ids_partidas_vencidas(df: pd.DataFrame, nome_personagem: str) -> list:
    """
    Retorna uma lista com os IDs das partidas vencidas por um personagem.
    """
    if 'vencedor' not in df.columns or 'id_partida' not in df.columns:
        raise ValueError("O DataFrame precisa conter as colunas 'vencedor' e 'id_partida'.")

    partidas_vencidas = df[df['vencedor'] == nome_personagem]
    return partidas_vencidas['id_partida'].tolist()


def contar_mortes_personagem(df: pd.DataFrame, nome_personagem: str) -> int:
    """
    Conta quantas vezes um personagem aparece como morto nas partidas.
    """
    contador = 0
    for linha in df['mortos']:
        try:
            mortos = json.loads(linha.replace('""', '"'))
            contador += mortos.count(nome_personagem)
        except Exception as e:
            print(f"Erro ao processar linha: {linha[:50]}... -> {e}")
    return contador


def exibir_estatisticas_personagem(historico_df: pd.DataFrame, personagem_nome: str, st_container=st):
    """
    Exibe as estatísticas do personagem, como vitórias, derrotas, ataques e habilidades.
    """
    # === Dados gerais ===
    qtd_mortes = contar_mortes_personagem(historico_df, personagem_nome)
    df_vitorias = historico_df[historico_df['vencedor'] == personagem_nome]

    total_partidas = qtd_mortes + len(df_vitorias)
    total_vitorias = len(df_vitorias)
    taxa_vitoria = (total_vitorias / total_partidas) * 100 if total_partidas else 0

    # === Logs de combate ===
    df_logs = converter_logs_em_df(historico_df['logs'].tolist())
    df_logs = df_logs[df_logs['atacante'] == personagem_nome]

    total_ataques = len(df_logs)
    ataques_bem_sucedidos = df_logs[df_logs['ataque_bem_sucedido'] == True]
    taxa_sucesso_ataque = (len(ataques_bem_sucedidos) / total_ataques) * 100 if total_ataques else 0

    media_dano = df_logs[df_logs['habilidade_ataque'] != 'Cura']['ataque_total'].mean() if total_ataques else 0

    habilidades_usadas = df_logs[df_logs['habilidade_ataque'].notna() & (df_logs['habilidade_ataque'] != "None")]
    taxa_uso_habilidade = (len(habilidades_usadas) / total_ataques) * 100 if total_ataques else 0

    habilidades_utilizadas = habilidades_usadas['habilidade_ataque'].value_counts().reset_index()
    habilidades_utilizadas.columns = ['habilidade', 'count']

    # === Exibição ===
    sc = st_container
    sc.markdown("### 📊 Estatísticas de Combate")
    sc.write(f"**Partidas:** {total_partidas}")
    sc.write(f"**Vitórias:** {total_vitorias}")
    sc.write(f"**Derrotas:** {qtd_mortes}")
    sc.write(f"**Taxa de Vitória:** {taxa_vitoria:.2f}%")
    sc.markdown("---")
    sc.write(f"**Ataques Realizados:** {total_ataques}")
    sc.write(f"**Ataques Bem-Sucedidos:** {len(ataques_bem_sucedidos)}")
    sc.write(f"**Taxa de Sucesso de Ataque:** {taxa_sucesso_ataque:.2f}%")
    sc.write(f"**Média de Dano por Ataque:** {media_dano:.2f}")
    sc.markdown("---")
    sc.write(f"**Habilidades Utilizadas:** {len(habilidades_usadas)}")
    sc.write(f"**Taxa de Uso de Habilidade:** {taxa_uso_habilidade:.2f}%")

    if not habilidades_utilizadas.empty:
        habilidade_top = habilidades_utilizadas.iloc[0]
        sc.write(f"**Habilidade Mais Utilizada:** {habilidade_top['habilidade']} ({habilidade_top['count']} vezes)")
    else:
        sc.write("**Habilidade Mais Utilizada:** Nenhuma")


# =====================================
# === Modal para Edição de Personagem
# =====================================

@st.dialog('Editar Personagem')
def modal_editar_personagem(personagem):
    """
    Modal de edição das habilidades do personagem.
    """
    habilidades_dict = st.session_state.gerenciamento.habilidades_dict
    chaves_habilidades = list(habilidades_dict.keys())

    limite = personagem.classe.limite_habilidades
    habilidades_selecionadas = []

    for c in range(limite):
        habilidade_atual = personagem.inventario[c] if c < len(personagem.inventario) else None
        habilidade_nome_atual = habilidade_atual.nome if habilidade_atual else None
        index_default = chaves_habilidades.index(habilidade_nome_atual) if habilidade_nome_atual in chaves_habilidades else 0

        habilidade_nome = st.selectbox(
            f'Habilidade {c + 1} de {limite}:',
            chaves_habilidades,
            index=index_default,
            key=f'{personagem.nome}_Habilidade_{c}'
        )
        habilidades_selecionadas.append(habilidades_dict.get(habilidade_nome))

    c1, c2, _ = st.columns([1, 1, 2])
    if c1.button('📥 Salvar', key=f'{personagem.nome}_salvar'):
        personagem.inventario = habilidades_selecionadas
        st.session_state.gerenciamento.editar_personagem(personagem.nome, personagem.classe, habilidades_selecionadas)
        st.rerun()

    if c2.button('🗑️ Excluir', key=f'{personagem.nome}_excluir'):
        st.session_state.gerenciamento.excluir_personagem(personagem)
        st.rerun()


# =====================================
# === Cartão Visual do Personagem
# =====================================

def criar_card_personagem(personagem, config_disabled=False):
    """
    Exibe um card com abas para visualizar, editar e ver estatísticas de um personagem.
    """
    with st.container(border=True, height=400):
        info, estatisticas, partidas_vencidas = st.tabs(['Informações', 'Estatísticas', 'Partidas Vencidas'])

        # Aba: Informações
        with info:
            img_col, info_col, ajustes_col = st.columns([1, 3, 0.5])
            with img_col:
                st.image(personagem.classe.foto)
            with info_col:
                st.write(f'#### {personagem.nome} - {personagem.classe.nome}')
            st.write(f'###### 🔋 :green[Vida:] {personagem.pontos_vida}')
            st.write(f'###### ⚔️ :red[Ataque:] {personagem.classe.pontos_ataque}')
            st.write(f'###### 🛡️ :blue[Defesa:] {personagem.pontos_defesa}')
            st.write(f':gray[Dado de Ataque:] {personagem.dado_ataque} | '
                     f':gray[Nº Habilidades:] {personagem.classe.limite_habilidades}')
            st.write(':gray[Set de Habilidades:]')

            if ajustes_col.button('⚙️', key=f'personagem_{personagem.nome}', disabled=config_disabled):
                modal_editar_personagem(personagem)

            cols = st.columns(5)
            for i, habilidade in enumerate(personagem.inventario):
                cols[i % 5].image(habilidade.foto_habilidade)

        # Aba: Estatísticas
        with estatisticas:
            df = pd.read_csv('data/historico_batalhas.csv').drop_duplicates()
            exibir_estatisticas_personagem(df, personagem.nome)

        # Aba: Partidas Vencidas
        with partidas_vencidas:
            df = pd.read_csv('data/historico_batalhas.csv').drop_duplicates()
            partidas_v = get_ids_partidas_vencidas(df, personagem.nome)
            if partidas_v:
                partida = st.pills('Selecione uma partida', partidas_v, key=f'{personagem.nome}_{partidas_v}')
                if partida:
                    st.session_state.id_partida = partida
                    st.switch_page('pages/relatorio_combate.py')
            else:
                st.warning(f'{personagem.nome} não venceu nenhuma partida')


# =====================================
# === Modal de Visualização Somente Leitura
# =====================================

@st.dialog('Visualização de personagem: ')
def modal_card_personagem(personagem):
    """
    Modal que exibe o personagem com informações bloqueadas (modo leitura).
    """
    criar_card_personagem(personagem, config_disabled=True)
