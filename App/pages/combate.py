import streamlit as st
import random
import base64
import json
import os
import pandas as pd

from RPG import *
from streamlit_avatar import avatar
from utils.streamlit_utils import (
    exportar_arenas_para_txt,
    get_image_base64,
    set_background_as_frame,
    exibir_avatar,
    resetar_estado_combate
)

# ==========================
# Utilitários
# ==========================




def exibir_logs_chat(logs):
    """
    Exibe os logs dinamicamente de combate em formato de chat.
    """
    with st.container(border=True, height=200):
        for remetente, mensagem in logs:
            role = "assistant" if remetente == "Sistema" else "user"
            with st.chat_message(role, avatar=None if role == "assistant" else "🧙"):
                st.markdown(f"**{remetente}:** {mensagem}", unsafe_allow_html=True)


def salvar_resultado_csv(arena: Arena, caminho_csv="data/historico_batalhas.csv"):
    """
    Salva o resultado da partida em um arquivo CSV.
    """
    if not arena.partidas:
        return

    partida = arena.partidas[-1]
    vivos = st.session_state.get("personagens_vivos", [])
    mortos = st.session_state.get("personagens_mortos", [])
    vencedor = arena.partida_atual.vencedor.nome

    linha = {
        "id_partida": partida.id,
        "vencedor": vencedor,
        "arena": arena.nome_arena,
        "mortos": json.dumps([p.nome for p in mortos], ensure_ascii=False),
        "logs": json.dumps([log.__dict__ for log in partida.logs], ensure_ascii=False)
    }

    df = pd.read_csv(caminho_csv) if os.path.exists(caminho_csv) else pd.DataFrame()
    if partida.id not in df["id_partida"].tolist():
        df = pd.concat([df, pd.DataFrame([linha])], ignore_index=True)
        df.to_csv(caminho_csv, index=False, encoding="utf-8")

    # Atualiza lista de personagens da arena com os atuais
    arena.lista_personagens = vivos + mortos

# ==========================
# Página de Combate
# ==========================

def pagina_combate(arena: Arena):
    """
    Página principal de combate. Controla a lógica do jogo, turnos e interface.
    """
    if not arena:
        st.warning("Nenhuma arena selecionada.")
        return

    set_background_as_frame(arena.foto_mapa)
    st.title(f"⚔️ Combate na Arena: {arena.nome_arena}")

    # Inicializa estado do combate se necessário
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

    # Referências rápidas
    vivos = st.session_state.personagens_vivos
    mortos = st.session_state.personagens_mortos
    logs = st.session_state.logs_visuais
    fila_turno = st.session_state.fila_turno

    # === Função Interna: Executar um turno ===
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

        if log.habilidade_ataque == 'Cura':
            msg = log.descricao_habilidade
        else:
            msg = f"atacou **{log.alvo}** com _{log.habilidade_ataque or 'ataque básico'}_ causando **{log.ataque_total} de dano**"

        logs.append((log.atacante, msg) if log.ataque_bem_sucedido else (log.atacante, f"tentou atacar **{log.alvo}** mas errou"))

        if alvo.pontos_vida <= 0 and alvo in vivos:
            vivos.remove(alvo)
            mortos.append(alvo)
            logs.append(("Sistema", f"☠️ **{alvo.nome}** foi derrotado!"))

        if atacante in vivos:
            fila_turno.append(atacante)

    # === Função: Combate completo até o fim ===
    def executar_combate_completo():
        while len(st.session_state.personagens_vivos) > 1:
            executar_turno()
        # Limpa a fila final
        st.session_state.fila_turno = [p for p in st.session_state.personagens_vivos if p.pontos_vida > 0]
        st.rerun()

    # === Layout ===
    c1, c2, c3 = st.columns([2, 1, 1.2])
    c1.markdown("### 📜 Registro de Combate")
    exibir_logs_chat(logs)

    combate_encerrado = len(vivos) == 1

    # === Encerramento de combate ===
    if combate_encerrado:

        arena.partida_atual.vencedor = vivos[0]
        salvar_resultado_csv(arena)
        st.markdown("## 🏁 Partida Encerrada")
        st.success("Verifique o relatório de combate")

        col_dowload, col_relatorio, col_reiniciar = st.columns(3)

        exportar_arenas_para_txt([arena], "data/historico_combate.txt")

        with open("data/historico_combate.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()

        col_dowload.download_button(
            label="📥 Baixar Histórico (.txt)",
            data=conteudo,
            file_name="data/historico_combate.txt",
            mime="text/plain"
        )

        if col_reiniciar.button("🔄 Reiniciar Partida"):
            resetar_estado_combate()
            st.rerun()

        if col_relatorio.button('📜 Relatório de combate'):
            st.switch_page('pages/relatorio_combate.py')

    # === Fila e Mortos ===
    col1, col2 = st.columns(2)
    with col1.container(border=True, height=300):
        st.markdown("### 🔝 Fila de Ataque")
        if fila_turno:
            avatar([exibir_avatar(p) for p in fila_turno])

    with col2.container(border=True, height=300):
        st.markdown(f"### 💀 Mortos ({len(mortos)}):")
        if mortos:
            avatar([exibir_avatar(p, morto=True) for p in mortos])

    # === Botões de ação ===
    if c2.button("▶️ Executar Turno", disabled=combate_encerrado):
        executar_turno()

    if c3.button("⏩️ Combate Completo", disabled=combate_encerrado):
        executar_combate_completo()
# ==========================
# Execução da Página
# ==========================
pagina_combate(st.session_state.get("arena_combate"))
