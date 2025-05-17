import streamlit as st
import random
import base64
import json
import os
import pandas as pd
from utils.streamlit_utils import exportar_arenas_para_txt, get_image_base64
from RPG import *
from streamlit_avatar import avatar

def exibir_resultado_csv(caminho_csv="data/historico_batalhas.csv", id_partida=st.session_state.id_partida):
    df = pd.read_csv(caminho_csv)
    linha = df.iloc[-1] if id_partida is None else df[df["id_partida"] == id_partida].iloc[0]
    qtd_partidas = len(df[df['arena'] == linha['arena']])
    st.title(f"Arena: {linha['arena']} — Partida {qtd_partidas}")

    vencedor_nome = linha["vencedor"]
    mortos_nomes = json.loads(linha["mortos"])
    logs = json.loads(linha["logs"])

    vencedor = next((p for p in st.session_state.personagens_lidos if p.nome == vencedor_nome), None)
    mortos = [p for p in st.session_state.personagens_lidos if p.nome in mortos_nomes]

    if vencedor:
        st.success(f"{vencedor.nome} subjulgou seus oponentes em batalha")
        avatar([{ "url": f"data:image/png;base64,{get_image_base64(vencedor.classe.foto)}", "size": 100, "title": vencedor.nome, "caption": f"👑 {vencedor.classe.nome}", "key": f"vencedor_{vencedor.nome}" }])

    st.markdown("### Mortos em Batalha")
    cols = st.columns(3)
    for i, p in enumerate(mortos):
        with cols[i % 3]:
            avatar([{"url": f"data:image/png;base64,{get_image_base64('./assets/images/morte.png')}", "size": 60, "title": p.nome, "caption": f"{p.classe.nome} ⚰️", "key": f"morto_{p.nome}" }])

    vivos, mortos_set = set(), set()
    if st.checkbox("Informações do combate"):
        with st.container(border=True, height=400):
            for log in logs:
                atacante, alvo = log["atacante"], log["alvo"]
                msg = log["descricao_habilidade"] if log["habilidade_ataque"] == "Cura" else f"atacou **{alvo}** com _{log['habilidade_ataque']}_ causando **{log['ataque_total']} de dano**"
                role = "assistant" if atacante.lower() == "sistema" else "user"

                with st.chat_message("user", avatar="🧙"):
                    st.markdown(f"**{atacante}:** {msg}", unsafe_allow_html=True)

                if log["alvo_vida"] <= 0 and alvo not in mortos_set:
                    mortos_set.add(alvo)
                    with st.chat_message("assistant"):
                        st.markdown(f"☠️ **{alvo}** foi derrotado!", unsafe_allow_html=True)

                vivos.update([atacante, alvo]) if log["alvo_vida"] > 0 else vivos.add(atacante)

            sobreviventes = vivos - mortos_set
            if len(sobreviventes) == 1:
                with st.chat_message("assistant"):
                    st.markdown(f"🏆 **{list(sobreviventes)[0]}** venceu a batalha!", unsafe_allow_html=True)
exibir_resultado_csv()