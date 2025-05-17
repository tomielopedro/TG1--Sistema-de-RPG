import streamlit as st
from RPG import *
import json
import base64
import pandas as pd
from streamlit_avatar import avatar


def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
def set_background_as_frame(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)


def exibir_avatar(personagem, morto=False):
    image_path = "assets/images/morte.png" if morto else personagem.classe.foto
    image_base64 = get_image_base64(image_path)
    image_url = f"data:image/png;base64,{image_base64}"
    caption = f'{personagem.classe.nome} ⚰️(Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})' if morto else f'{personagem.classe.nome} (Vida:️ {personagem.pontos_vida} Habilidades: {len(personagem.inventario)})'
    return {"url": image_url, "size": 60, "title": personagem.nome, "caption": caption, "key": f"{'morto' if morto else 'vivo'}_{personagem.nome}"}

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



def exportar_resultado_batalha_json(arena: Arena, caminho: str = "data/resultado_batalha.json"):
    if not arena.partidas:
        return

    partida = arena.partidas[-1]  # Última partida
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
        "mapa": arena.mapa,
        "vencedor": {
            "nome": vencedor.nome,
            "classe": vencedor.classe.nome
        } if vencedor else None,
        "mortos": mortos,
        "logs": logs_formatados
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

def get_ids_partidas_vencidas(df: pd.DataFrame, nome_personagem: str):

    if 'vencedor' not in df.columns or 'id_partida' not in df.columns:
        raise ValueError("O DataFrame precisa conter as colunas 'vencedor' e 'id_partida'.")

    partidas_vencidas = df[df['vencedor'] == nome_personagem]
    return partidas_vencidas['id_partida'].tolist()

def get_ids_partidas_arena(df: pd.DataFrame, nome_arena: str):

    if 'arena' not in df.columns or 'id_partida' not in df.columns:
        raise ValueError("O DataFrame precisa conter as colunas 'arena' e 'id_partida'.")

    partidas_vencidas = df[df['arena'] == nome_arena]
    return partidas_vencidas['id_partida'].tolist()

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

def contar_mortes_personagem(df: pd.DataFrame, nome_personagem: str) -> int:
    contador = 0
    for linha in df['mortos']:
        try:
            mortos = json.loads(linha.replace('""', '"'))
            contador += mortos.count(nome_personagem)
        except Exception as e:
            print(f"Erro ao processar linha: {linha[:50]}... -> {e}")
    return contador
def exibir_estatisticas_arena(historico_df: pd.DataFrame, nome_arena: str, st_container=st):

    sc = st_container
    df_arena = historico_df[historico_df['arena'] == nome_arena]

    if df_arena.empty:
        sc.warning(f"Nenhuma partida encontrada para a arena '{nome_arena}'.")
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


def exibir_estatisticas_personagem(historico_df: pd.DataFrame, personagem_nome: str, st_container=st):
    # === Partidas, vitórias, derrotas ===
    qtd_mortes = contar_mortes_personagem(historico_df, personagem_nome)
    df_vitorias = historico_df[historico_df['vencedor'] == personagem_nome]

    total_partidas = qtd_mortes + len(df_vitorias)
    total_vitorias = len(df_vitorias)
    total_derrotas = qtd_mortes
    taxa_vitoria = (total_vitorias / total_partidas) * 100 if total_partidas else 0

    # === Logs de combate ===
    df_logs = converter_logs_em_df(historico_df['logs'].tolist())
    df_logs = df_logs[df_logs['atacante'] == personagem_nome]

    total_ataques = len(df_logs)
    ataques_bem_sucedidos = df_logs[df_logs['ataque_bem_sucedido'] == True]
    taxa_sucesso_ataque = (len(ataques_bem_sucedidos) / total_ataques) * 100 if total_ataques else 0
    media_dano = df_logs[df_logs['habilidade_ataque'] != 'Cura']
    media_dano = media_dano['ataque_total'].mean() if total_ataques else 0

    habilidades_usadas = df_logs[df_logs['habilidade_ataque'].notna() & (df_logs['habilidade_ataque'] != "None")]
    total_habilidades_usadas = len(habilidades_usadas)
    taxa_uso_habilidade = (total_habilidades_usadas / total_ataques) * 100 if total_ataques else 0

    habilidades_utilizadas = habilidades_usadas['habilidade_ataque'].value_counts().reset_index()
    habilidades_utilizadas.columns = ['habilidade', 'count']

    # === Exibição ===
    sc = st_container  # atalho
    sc.markdown("### 📊 Estatísticas de Combate")
    sc.write(f"**Partidas:** {total_partidas}")
    sc.write(f"**Vitórias:** {total_vitorias}")
    sc.write(f"**Derrotas:** {total_derrotas}")
    sc.write(f"**Taxa de Vitória:** {taxa_vitoria:.2f}%")
    sc.markdown("---")
    sc.write(f"**Ataques Realizados:** {total_ataques}")
    sc.write(f"**Ataques Bem-Sucedidos:** {len(ataques_bem_sucedidos)}")
    sc.write(f"**Taxa de Sucesso de Ataque:** {taxa_sucesso_ataque:.2f}%")
    sc.write(f"**Média de Dano por Ataque:** {media_dano:.2f}")
    sc.markdown("---")
    sc.write(f"**Habilidades Utilizadas:** {total_habilidades_usadas}")
    sc.write(f"**Taxa de Uso de Habilidade:** {taxa_uso_habilidade:.2f}%")

    if not habilidades_utilizadas.empty:
        habilidade_top = habilidades_utilizadas.iloc[0]
        sc.write(f"**Habilidade Mais Utilizada:** {habilidade_top['habilidade']} ({habilidade_top['count']} vezes)")
    else:
        sc.write("**Habilidade Mais Utilizada:** Nenhuma")


def criar_card_personagem(personagem):
    with st.container(border=True, height=400):
        info, estatisticas, partidas_vencidas = st.tabs(['Informações', 'Estatísticas', 'Partidas Vencidas'])

        with info:
            img_col, info_col, ajustes_col = st.columns([1, 3, 0.5])

            # Imagem
            with img_col:
                st.image(personagem.classe.foto, width=100)

            # Nome e Classe
            with info_col:
                st.write(f'#### {personagem.nome} - {personagem.classe.nome}')

            # Atributos
            st.write(f'###### 🔋 :green[Vida:] {personagem.pontos_vida}')
            st.write(f'###### ⚔️ :red[Ataque:] {personagem.classe.pontos_ataque}')
            st.write(f'###### 🛡️ :blue[Defesa:] {personagem.pontos_defesa}')
            st.write(f':gray[Dado de Ataque:] {personagem.dado_ataque} | '
                     f':gray[Nº Habilidades:] {personagem.classe.limite_habilidades}')

            # Set de Habilidades
            st.write(':gray[Set de Habilidades:]')
            if ajustes_col.button('⚙️', key=f'personagem_{personagem.nome}'):
                st.balloons()

            cols = st.columns(5)
            for i, habilidade in enumerate(personagem.inventario):
                cols[i % 5].image(habilidade.foto_habilidade, width=100)
        df = pd.read_csv('data/historico_batalhas.csv')
        df = df.drop_duplicates()
        with estatisticas:
            exibir_estatisticas_personagem(df, personagem.nome)
        with partidas_vencidas:
            partidas_vencidas = get_ids_partidas_vencidas(df, personagem.nome)
            partida = st.pills('Selecione uma partida', partidas_vencidas, key=partidas_vencidas)
            if partida:
                st.session_state.id_partida = partida
                st.switch_page('pages/_relatorio_combate.py')





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
        informacoes, estatisticas, partidas = st.tabs(['Informações', 'Estatísticas', 'Partidas'])
        with informacoes:
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
        df = pd.read_csv('data/historico_batalhas.csv')

        with estatisticas:
            exibir_estatisticas_arena(df, arena.nome_arena)
        with partidas:
            partidas_realizadas = get_ids_partidas_arena(df, arena.nome_arena)
            partida = st.pills('Selecione uma partida', partidas_realizadas, key=partidas_realizadas)
            if partida:
                st.session_state.id_partida = partida
                st.switch_page('pages/_relatorio_combate.py')


    if st.button('🚪 Entrar na arena', key=f'Combate_{arena.nome_arena}', use_container_width=True, type='primary'):
        st.session_state.arena_combate = arena
        st.session_state.arena_combate.lista_personagens = [p.__copy__() for p in st.session_state.arena_combate.lista_personagens]
        st.switch_page("pages/combate.py")



