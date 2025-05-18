import streamlit as st
import base64
import json
import pandas as pd
from typing import List
from RPG import *
import os
from datetime import datetime

# ==============================
# === Estilo e Visual da Página
# ==============================
import streamlit as st

def carregar_logs(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return f.readlines()

def exibir_logs_chat_generico(caminho_arquivo, titulo="📜 Logs"):
    """
    Exibe logs de forma estilizada como um chat, com suporte para logs de arenas ou personagens.

    Args:
        caminho_arquivo (str): Caminho para o arquivo de log.
        titulo (str): Título a ser exibido acima do botão de download.
    """
    st.title(titulo)

    # Botão de download
    with open(caminho_arquivo, "rb") as f:
        st.download_button(
            label="📥 Baixar Arquivo de Logs",
            data=f,
            file_name=caminho_arquivo.split("/")[-1],
            mime="text/plain"
        )

    # Carrega e processa logs
    if st.checkbox('Visualizar logs'):
        logs = carregar_logs(caminho_arquivo)
        logs = logs[-100:]
        with st.container(height=400):
            for linha in logs:
                linha = linha.strip()
                if not linha:
                    continue

                # Define tipo de mensagem com emoji
                if "Erro" in linha:
                    emoji = "🟥"
                elif "Aviso" in linha:
                    emoji = "🟨"
                else:
                    emoji = "ℹ️"

                # Extrai timestamp, nome e mensagem
                try:
                    timestamp_fim = linha.find("]")
                    timestamp_str = linha[1:timestamp_fim]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    data_formatada = timestamp.strftime("%d/%m/%Y %H:%M")

                    restante = linha[timestamp_fim + 2:]
                    nome_inicio = restante.find("[") + 1
                    nome_fim = restante.find("]")
                    nome = restante[nome_inicio:nome_fim]

                    mensagem = restante[nome_fim + 2:].strip()
                except Exception:
                    nome = "Desconhecido"
                    data_formatada = "Data inválida"
                    mensagem = linha

                with st.chat_message("user", avatar="🧙‍♂️"):
                    st.markdown(f"**🗓️ {data_formatada} — {nome}**\n\n{emoji} {mensagem}")
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get_image_path(relative_path):
    return os.path.join(get_project_root(), relative_path)

# Exemplo
def set_background_as_frame(image_path: str):
    """
    Define a imagem de fundo da aplicação em tela cheia com CSS inline.
    """
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            div[data-testid="stVerticalBlock"] {{
                padding-top: 0rem !important;
            }}
            .block-container {{
                background-color: #101414;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 0 0px rgba(0, 0, 0, 0.1);
                margin-top: 5rem;
            }}
            .st-emotion-cache-h4xjwg,
            .st-emotion-cache-12fmjuu {{
                height: 0rem;
            }}
            .stApp {{
            background: url("data:image/png;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}
            </style>
        """, unsafe_allow_html=True)


def get_image_base64(image_path: str) -> str:
    """
    Converte uma imagem para string Base64 para uso inline no HTML.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# ==============================
# === Avatares e Exibição
# ==============================

def exibir_avatar(personagem: Personagem, morto: bool = False) -> dict:
    """
    Gera o dicionário necessário para exibir um avatar customizado com informações do personagem.
    """
    image_path = get_image_path("assets/images/extras/morte.png") if morto else personagem.classe.foto
    image_base64 = get_image_base64(image_path)
    image_url = f"data:image/png;base64,{image_base64}"
    caption = (
        f'{personagem.classe.nome} ⚰️(Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})'
        if morto else
        f'{personagem.classe.nome} (Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})'
    )
    return {
        "url": image_url,
        "size": 60,
        "title": personagem.nome,
        "caption": caption,
        "key": f"{'morto' if morto else 'vivo'}_{personagem.nome}"
    }

# ==============================
# === Exportações de Dados
# ==============================

def exportar_arenas_para_txt(arenas: List['Arena'], caminho: str = "data/historico_arenas.txt"):
    """
    Exporta as informações completas das arenas e suas partidas para um arquivo .txt.
    """
    with open(caminho, "w", encoding="utf-8") as f:
        for arena in arenas:
            f.write(f"=== Arena: {arena.nome_arena} ===\n")
            f.write(f"Tipo: {arena.tipo_jogo} | Mapa: {arena.mapa.nome_mapa}\n\n")

            for partida in arena.partidas:
                f.write(f"--- Partida {partida.id}: {partida.descricao} ---\n")
                f.write(f'Vencedor: -- {partida.vencedor} -- \n')
                for log in partida.logs:
                    f.write(
                        f"[Log] {log.atacante} ({log.atacante_classe}) atacou {log.alvo} ({log.alvo_classe})\n"
                        f"  D20: {log.numero_d20} | Dano Total: {log.ataque_total} | "
                        f"Defesa do Alvo: {log.alvo_pontos_defesa} | "
                        f"Habilidade: {log.habilidade_ataque} | "
                        f"Vida do Alvo após ataque: {log.alvo_vida}\n"
                    )
                f.write("\n")
            f.write("\n")


def exportar_resultado_batalha_json(arena: Arena, caminho: str = "data/resultado_batalha.json"):
    """
    Exporta o resultado final de uma batalha da arena em formato JSON estruturado.
    """
    if not arena.partidas:
        return

    partida = arena.partidas[-1]
    vencedor = None
    mortos = []

    for personagem in arena.lista_personagens:
        if personagem.pontos_vida > 0:
            vencedor = personagem
        else:
            mortos.append({
                "nome": personagem.nome,
                "classe": personagem.classe.nome
            })

    logs_formatados = []
    for log in partida.logs:
        logs_formatados.append({
            "atacante": log.atacante,
            "atacante_classe": log.atacante_classe,
            "alvo": log.alvo,
            "alvo_classe": log.alvo_classe,
            "alvo_vida_restante": log.alvo_vida,
            "alvo_pontos_defesa": log.alvo_pontos_defesa,
            "numero_d20": log.numero_d20,
            "chance_ataque": log.chance_ataque,
            "ataque_bem_sucedido": log.ataque_bem_sucedido,
            "ataque_total": log.ataque_total,
            "habilidade_ataque": log.habilidade_ataque,
            "descricao_habilidade": log.descricao_habilidade
        })

    resultado = {
        "arena": arena.nome_arena,
        "tipo_jogo": arena.tipo_jogo,
        "mapa": arena.mapa.nome_mapa,
        "vencedor": {
            "nome": vencedor.nome,
            "classe": vencedor.classe.nome
        } if vencedor else None,
        "mortos": mortos,
        "logs": logs_formatados
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

# ==============================
# === Manipulação de Logs
# ==============================

def converter_logs_em_df(lista_logs_str: List[str]) -> pd.DataFrame:
    """
    Converte uma lista de strings de logs JSON para um DataFrame estruturado.
    """
    logs_processados = []
    for log_str in lista_logs_str:
        try:
            log_corrigido = log_str.replace('""', '"')
            logs = json.loads(log_corrigido)
            logs_processados.extend(logs)
        except Exception as e:
            print(f"Erro ao processar log: {log_str[:100]}... -> {e}")
    return pd.DataFrame(logs_processados)

# ==============================
# === Estado do Combate
# ==============================

def resetar_estado_combate():
    """
    Remove todas as variáveis de estado relacionadas ao combate para reinício da partida.
    Reinstancia os personagens com vida e habilidades completas.
    """
    if st.session_state.arena_combate is not None:
        for chave in ["personagens_vivos", "personagens_mortos", "logs_visuais", "turno", "fila_turno"]:
            st.session_state.pop(chave, None)

        personagens_novos = [
            p.__copy__() for p in st.session_state.personagens_lidos
            if p in st.session_state.arena_combate.lista_personagens
        ]
        st.session_state.arena_combate.lista_personagens = personagens_novos
