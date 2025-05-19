import streamlit as st
from datetime import datetime
import os
import json
import pandas as pd


def carregar_logs(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return f.readlines()


def exibir_logs_chat_generico(caminho_arquivo, titulo="📜 Logs"):
    st.title(titulo)
    with open(caminho_arquivo, "rb") as f:
        st.download_button("📥 Baixar Arquivo de Logs", f, file_name=os.path.basename(caminho_arquivo), mime="text/plain")

    if st.checkbox('Visualizar logs'):
        logs = carregar_logs(caminho_arquivo)[-100:]
        with st.container(height=400):
            for linha in logs:
                linha = linha.strip()
                if not linha:
                    continue
                emoji = "🟥" if "Erro" in linha else "🟨" if "Aviso" in linha else "ℹ️"
                try:
                    timestamp_str = linha[1:linha.find("]")]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    data_formatada = timestamp.strftime("%d/%m/%Y %H:%M")

                    restante = linha[linha.find("]") + 2:]
                    nome = restante[restante.find("[") + 1:restante.find("]")]
                    mensagem = restante[restante.find("]") + 2:]
                except:
                    data_formatada, nome, mensagem = "Data inválida", "Desconhecido", linha

                with st.chat_message("user", avatar="🧙‍♂️"):
                    st.markdown(f"**🗓️ {data_formatada} — {nome}**\n\n{emoji} {mensagem}")


def converter_logs_em_df(lista_logs_str):
    logs_processados = []
    for log_str in lista_logs_str:
        try:
            log_corrigido = log_str.replace('""', '"')
            logs = json.loads(log_corrigido)
            logs_processados.extend(logs)
        except Exception as e:
            print(f"Erro ao processar log: {log_str[:100]}... -> {e}")
    return pd.DataFrame(logs_processados)
