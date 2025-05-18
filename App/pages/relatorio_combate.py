import streamlit as st
import pandas as pd
import json
from utils.streamlit_utils import get_image_base64, set_background_as_frame
from streamlit_avatar import avatar
from RPG import *

# ==============================
# Utilitários de Batalha
# ==============================


def carregar_dados_partida(caminho_csv: str, id_partida=None) -> dict:
    """
    Lê o CSV de partidas e retorna os dados correspondentes à última ou à partida com o ID especificado.
    """
    df = pd.read_csv(caminho_csv)
    if not df.empty:
        linha = df.iloc[-1] if id_partida is None else df[df["id_partida"] == id_partida].iloc[0]
        return {
            "linha": linha,
            "qtd_partidas": len(df[df['arena'] == linha['arena']])
        }



def obter_personagens_partida(linha: pd.Series) -> tuple:
    """
    Mapeia os nomes de personagens da linha para os objetos carregados na sessão.
    """
    vencedor_nome = linha["vencedor"]
    mortos_nomes = json.loads(linha["mortos"])

    vencedor = next((p for p in st.session_state.personagens_lidos if p.nome == vencedor_nome), None)
    mortos = [p for p in st.session_state.personagens_lidos if p.nome in mortos_nomes]

    return vencedor, mortos


def exibir_cabecalho_partida(arena_nome: str, partida_num: int, vencedor: Personagem, mortos: list[Personagem]):
    """
    Exibe o cabeçalho da partida com título, vencedor e personagens mortos.
    """
    st.title(f"Arena: {arena_nome} — Partida {partida_num}")

    if vencedor:
        st.success(f"{vencedor.nome} subjulgou seus oponentes em batalha")
        avatar([{
            "url": f"data:image/png;base64,{get_image_base64(vencedor.classe.foto)}",
            "size": 100,
            "title": vencedor.nome,
            "caption": f"👑 {vencedor.classe.nome}",
            "key": f"vencedor_{vencedor.nome}"
        }])

    st.markdown("### Mortos em Batalha")
    cols = st.columns(3)
    for i, p in enumerate(mortos):
        with cols[i % 3]:
            avatar([{
                "url": f"data:image/png;base64,{get_image_base64('./assets/images/extras/morte.png')}",
                "size": 60,
                "title": p.nome,
                "caption": f"{p.classe.nome} ⚰️",
                "key": f"morto_{p.nome}"
            }])


def exibir_logs_combate(logs: list[dict]):
    """
    Exibe os eventos de combate em formato de chat, incluindo cura, ataques e derrotas.
    """

    vivos, mortos_set = set(), set()

    with st.container(border=True, height=400):
        for log in logs:
            atacante = log["atacante"]
            alvo = log["alvo"]

            # Descrição do ataque
            msg = log["descricao_habilidade"] if log["habilidade_ataque"] == "Cura" else \
                f"atacou **{alvo}** com _{log['habilidade_ataque'] or 'ataque básico'}_ causando **{log['ataque_total']} de dano**"

            with st.chat_message("user", avatar="🧙"):
                st.markdown(f"**{atacante}:** {msg}", unsafe_allow_html=True)

            # Se o alvo morreu
            if log["alvo_vida"] <= 0 and alvo not in mortos_set:
                mortos_set.add(alvo)
                with st.chat_message("assistant"):
                    st.markdown(f"☠️ **{alvo}** foi derrotado!", unsafe_allow_html=True)

            # Registro de vivos
            if log["alvo_vida"] > 0:
                vivos.update([atacante, alvo])
            else:
                vivos.add(atacante)

        # Vencedor final
        sobreviventes = vivos - mortos_set
        if len(sobreviventes) == 1:
            vencedor = list(sobreviventes)[0]
            with st.chat_message("assistant"):
                st.markdown(f"🏆 **{vencedor}** venceu a batalha!", unsafe_allow_html=True)





# ==============================
# Função principal
# ==============================

def exibir_resultado_csv(caminho_csv="data/historico_batalhas.csv", id_partida=None):

    """
    Exibe o resultado completo de uma partida, incluindo vencedor, mortos e logs de combate.
    """
    dados = carregar_dados_partida(caminho_csv, id_partida or st.session_state.get("id_partida"))
    if not dados:
        return st.warning('Nenhum dado encontrado')
    linha = dados["linha"]
    set_background_as_frame('./assets/images/extras/fundo_tela_inicial.png')

    vencedor, mortos = obter_personagens_partida(linha)

    exibir_cabecalho_partida(
        arena_nome=linha["arena"],
        partida_num=dados["qtd_partidas"],
        vencedor=vencedor,
        mortos=mortos
    )

    logs = json.loads(linha["logs"])
    if st.checkbox("Informações do combate"):
        exibir_logs_combate(logs)


# ==============================
# Execução da visualização
# ==============================

exibir_resultado_csv()
