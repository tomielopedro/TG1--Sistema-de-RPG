import streamlit as st
import random
import base64
import json
import os
import pandas as pd
from utils.streamlit_utils import exportar_arenas_para_txt, get_image_base64, set_background_as_frame, exibir_avatar
from RPG import *
from streamlit_avatar import avatar

# ==========================
# Estilos
# ==========================
st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] {
        padding-top: 0rem !important;
    }
    .block-container {
        background-color: #101414;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 0px rgba(0, 0, 0, 0.1);
        margin-top: 5rem;
    }
    .st-emotion-cache-h4xjwg,
    .st-emotion-cache-12fmjuu {
        height: 0rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================
# Utilitários
# ==========================
def resetar_estado_combate():
    for chave in ["personagens_vivos", "personagens_mortos", "logs_visuais", "turno", "fila_turno"]:
        st.session_state.pop(chave, None)

    if "arena_combate" in st.session_state:
        personagens_novos = [p.__copy__() for p in st.session_state.personagens_lidos if p in st.session_state.arena_combate.lista_personagens]
        st.session_state.arena_combate.lista_personagens = personagens_novos





def exibir_logs_chat(logs):
    with st.container(border=True, height=200):
        for remetente, mensagem in logs:
            role = "assistant" if remetente == "Sistema" else "user"
            with st.chat_message(role, avatar=None if role == "assistant" else "🧙"):
                st.markdown(f"**{remetente}:** {mensagem}", unsafe_allow_html=True)

# ==========================
# Resultado e Relatório
# ==========================
def salvar_resultado_csv(arena: Arena, caminho_csv="data/historico_batalhas.csv"):
    if not arena.partidas:
        return

    partida = arena.partidas[-1]
    vivos = st.session_state.get("personagens_vivos", [])
    mortos = st.session_state.get("personagens_mortos", [])
    vencedor = vivos[0].nome if len(vivos) == 1 else None
    mortos_nomes = [p.nome for p in mortos]
    logs_dicts = [log.__dict__ for log in partida.logs]

    linha = {
        "id_partida": partida.id,
        "vencedor": vencedor,
        "arena": arena.nome_arena,
        "mortos": json.dumps(mortos_nomes, ensure_ascii=False),
        "logs": json.dumps(logs_dicts, ensure_ascii=False)
    }

    df = pd.read_csv(caminho_csv) if os.path.exists(caminho_csv) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([linha])], ignore_index=True)
    df.to_csv(caminho_csv, index=False, encoding="utf-8")

    arena.lista_personagens = vivos + mortos


# ==========================
# Página de Combate
# ==========================
def pagina_combate(arena):
    if not arena:
        st.warning("Nenhuma arena selecionada.")
        return

    set_background_as_frame("./assets/images/maps/torre.png")
    st.title(f"⚔️ Combate na Arena: {arena.nome_arena}")

    if "personagens_vivos" not in st.session_state:
        personagens_copia = [p.__copy__() for p in arena.lista_personagens]
        st.session_state.update({
            "personagens_vivos": personagens_copia,
            "personagens_mortos": [],
            "logs_visuais": [],
            "turno": 1,
            "fila_turno": personagens_copia.copy()
        })
        arena.iniciar_nova_partida("Batalha Total")

    vivos, mortos, logs, fila_turno = st.session_state.personagens_vivos, st.session_state.personagens_mortos, st.session_state.logs_visuais, st.session_state.fila_turno

    def executar_turno():
        fila_turno[:] = [p for p in fila_turno if p in vivos]
        if not fila_turno:
            fila_turno.extend(vivos)
            st.session_state.turno += 1
            logs.append(("Sistema", f"--- Início do Turno {st.session_state.turno} ---"))

        atacante = fila_turno.pop(0)
        alvos = [p for p in vivos if p != atacante]
        if not alvos:
            return
        alvo = random.choice(alvos)
        log = arena.combate(atacante, alvo)
        arena.partida_atual.adicionar_log(log)

        msg = log.descricao_habilidade if log.habilidade_ataque == 'Cura' else f"atacou **{log.alvo}** com _{log.habilidade_ataque or 'ataque básico'}_ causando **{log.ataque_total} de dano**"
        logs.append((log.atacante, msg) if log.ataque_bem_sucedido else (log.atacante, f"tentou atacar **{log.alvo}** mas errou"))

        if alvo.pontos_vida <= 0 and alvo in vivos:
            vivos.remove(alvo)
            mortos.append(alvo)
            logs.append(("Sistema", f"☠️ **{alvo.nome}** foi derrotado!"))
        if atacante in vivos:
            fila_turno.append(atacante)

    # === Layout ===
    c1, c2, c3 = st.columns([2, 1, 1.2])
    c1.markdown("### 📜 Registro de Combate")
    exibir_logs_chat(logs)

    disabled = len(vivos) == 1

    if disabled:
        exportar_arenas_para_txt([arena], "historico_combate.txt")
        with open("historico_combate.txt", "r", encoding="utf-8") as f:
            st.sidebar.download_button("📥 Baixar Histórico (.txt)", f, file_name="historico_combate.txt")
        salvar_resultado_csv(arena)

        st.markdown("## 🏁 Partida Encerrada")
        st.success(f"Verifique o relatório da partida")

        col_relatorio, col_reiniciar = st.columns(2)
        if col_reiniciar.button("🔄 Reiniciar Partida"):
            resetar_estado_combate()
            st.rerun()

        if col_relatorio.button('Relatório de combate'):
            st.switch_page('pages/_relatorio_combate.py')

    col1, col2 = st.columns(2)
    with col1.container(border=True, height=300):
        st.markdown("### 🔝 Fila de Ataque")
        if fila_turno:
            avatar([exibir_avatar(p) for p in fila_turno])

    with col2.container(border=True, height=300):
        st.markdown(f"### 💀 Mortos ({len(mortos)}):")
        for p in mortos:
            avatar([exibir_avatar(p, morto=True)])

    if c2.button("▶️ Executar Turno", disabled=disabled):
        executar_turno()

    if c3.button("⏩️ Combate Completo", disabled=disabled):
        while len(vivos) > 1:
            executar_turno()

# ==========================
# Execução
# ==========================
pagina_combate(st.session_state.get("arena_combate"))
