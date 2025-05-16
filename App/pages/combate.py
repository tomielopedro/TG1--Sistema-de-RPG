import streamlit as st
import random
from utils.streamlit_utils import exportar_arenas_para_txt, criar_card_personagem
from RPG import *
from streamlit_avatar import avatar
import base64

# === Utilitário de imagem ===
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def set_background_as_frame(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
    <style>

    /* Estiliza o container vertical principal */
    .block-container {
        background-color: #101414;
        padding: 1rem 1rem;
        border-radius: 8px;
        box-shadow: 0 0 0px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    .st-emotion-cache-h4xjwg{
    height:0rem;}
    
    .st-emotion-cache-12fmjuu{
    height:0rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Funções auxiliares ===
def exibir_avatar(personagem, morto=False):
    if morto:
        image_path = "assets/images/morte.png"
    else:
        image_path = personagem.classe.foto
    image_base64 = get_image_base64(image_path)
    image_url = f"data:image/png;base64,{image_base64}"
    caption = f'{personagem.classe.nome} ⚰️(Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})' if morto else f'{personagem.classe.nome} (Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})'
    return {"url": image_url, "size": 60, "title": personagem.nome, "caption": caption, "key": f"{'morto' if morto else 'vivo'}_{personagem.nome}"}

def exibir_logs_chat(logs):
    with st.container(border=True, height=200):
        for remetente, mensagem in logs:
            role = "assistant" if remetente == "Sistema" else "user"
            with st.chat_message(role, avatar=None if role == "assistant" else "🧙"):
                st.markdown(f"**{remetente}:** {mensagem}", unsafe_allow_html=True)

# === Página principal de combate ===
def pagina_combate(arena):
    set_background_as_frame("./assets/images/maps/torre.png")
    st.title(f"⚔️ Combate na Arena: {arena.nome_arena}")

    if "personagens_vivos" not in st.session_state:
        st.session_state.personagens_vivos = arena.lista_personagens.copy()
        st.session_state.personagens_mortos = []
        st.session_state.logs_visuais = []
        st.session_state.turno = 1
        st.session_state.fila_turno = arena.lista_personagens.copy()
        arena.iniciar_nova_partida("Batalha Total")

    vivos = st.session_state.personagens_vivos
    mortos = st.session_state.personagens_mortos
    logs = st.session_state.logs_visuais
    fila_turno = st.session_state.fila_turno

    if len(vivos) <= 1:
        if vivos:
            vencedor = vivos[0]
            if not logs or "venceu" not in logs[-1][1]:
                logs.append(("Sistema", f"🏆 {vencedor} venceu a batalha!"))
            st.success(f"{vencedor.nome} subjulgou seus oponentes em batalha")
            image_url = f"data:image/png;base64,{get_image_base64(vencedor.classe.foto)}"
            avatar([{
                "url": image_url, "size": 100, "title": vencedor.nome,
                "caption": f"👑 {vencedor.classe.nome} (Vida:️ {vencedor.pontos_vida} Habilidades: {len(vencedor.inventario)})",
                "key": f"vencedor_{vencedor.nome}"
            }])
            with st.container(height=200, border=True):
                st.write(f"# 🪦 Mortos em batalha")
                cols = st.columns(3)
                for i, personagem in enumerate(mortos):
                    with cols[i % 3]:
                        avatar([exibir_avatar(personagem, morto=True)])

        with st.expander('📜 Registro de combate'):
            exibir_logs_chat(logs)

        exportar_arenas_para_txt([arena], "historico_combate.txt")
        with open("historico_combate.txt", "r", encoding="utf-8") as f:
            st.sidebar.download_button("📥 Baixar Histórico (.txt)", f, file_name="historico_combate.txt")
        return

    with st.sidebar:
        st.markdown("## 🎬 Executar Ação")
        if st.button("▶️ Executar Turno"):
            fila_turno[:] = [p for p in fila_turno if p in vivos]
            if not fila_turno:
                fila_turno.extend(vivos)
                st.session_state.turno += 1
                logs.append(("Sistema", f"--- 🌀 Início do Turno {st.session_state.turno} ---"))

            atacante = fila_turno.pop(0)
            alvos_possiveis = [p for p in vivos if p != atacante]
            if not alvos_possiveis:
                st.warning("Só resta um personagem!")
                return

            alvo = random.choice(alvos_possiveis)
            log = arena.combate(atacante, alvo)
            arena.partida_atual.adicionar_log(log)

            if log.ataque_bem_sucedido:
                texto_log = (
                    log.descricao_habilidade if log.habilidade_ataque == 'Cura' else
                    f"atacou **{log.alvo}** ({log.alvo_classe}) com sucesso! "
                    f"usando _{log.habilidade_ataque or 'ataque básico'}_ "
                    f"causando **{log.ataque_total} de dano**"
                )
            else:
                texto_log = f"tentou atacar **{log.alvo}** mas errou"
            logs.append((log.atacante, texto_log))

            if alvo.pontos_vida <= 0 and alvo in vivos:
                vivos.remove(alvo)
                mortos.append(alvo)
                logs.append(("Sistema", f"☠️ **{alvo.nome}** foi derrotado!"))

            if atacante in vivos:
                fila_turno.append(atacante)

    st.markdown("## 📜 Registro de Combate")
    st.write(f'#### 🔄 Turno {st.session_state.turno}')
    exibir_logs_chat(logs)

    col1, col2 = st.columns(2)
    with col1.container(border=True, height=300):
        st.markdown("### 🔝 Fila de Ataque")
        if fila_turno:
            fila_visual = [exibir_avatar(p) for p in fila_turno]
            avatar(fila_visual)

    with col2.container(border=True, height=300):
        st.markdown(f"### 💀 Mortos ({len(mortos)}):")
        for p in mortos:
            avatar([exibir_avatar(p, morto=True)])



# === Execução da página ===
if st.session_state.arena_combate:
    pagina_combate(st.session_state.arena_combate)
else:
    st.warning("Nenhuma arena selecionada.")
