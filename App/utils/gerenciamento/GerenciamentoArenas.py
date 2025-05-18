from RPG import *
import streamlit as st

class GerenciamentoArenas:
    """
    Classe singleton responsável por gerenciar a criação, edição, exclusão e leitura de arenas de combate.

    Atributos de Classe:
        _instance (GerenciamentoArenas): Instância única da classe.
        _lista_arenas (List[Arena]): Lista de todas as arenas gerenciadas.

    Atributos de Instância:
        arquivo (str): Caminho do arquivo onde arenas são persistidas.
        mapas_dict (dict): Dicionário de mapas disponíveis.
        tipo_dict (dict): Dicionário de tipos de jogo disponíveis.

    Métodos:
        get_arenas(): Retorna a lista de arenas.
        salvar_arena(): Cria e salva uma nova arena no arquivo e na memória.
        editar_arena(): Edita uma arena existente.
        excluir_arena(): Remove uma arena da lista e do arquivo.
        ler_arenas(): Lê as arenas do arquivo e as carrega na memória.
    """

    _instance = None
    _lista_arenas = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciamentoArenas, cls).__new__(cls)
        return cls._instance

    def __init__(self, arquivo, mapas_dict, tipo_dict):
        """
        Inicializa o gerenciador de arenas (singleton).

        Args:
            arquivo (str): Caminho do arquivo de arenas.
            mapas_dict (dict): Dicionário de mapas disponíveis.
            tipo_dict (dict): Dicionário de tipos de jogo disponíveis.
        """
        if not hasattr(self, '_initialized'):
            self.arquivo = arquivo
            self._initialized = True
            self.mapas_dict = mapas_dict
            self.tipo_dict = tipo_dict
            self.ler_arenas()

    @classmethod
    def get_arenas(cls):
        """
        Retorna a lista de arenas gerenciadas.

        Returns:
            list: Lista de instâncias da classe Arena.
        """
        return cls._lista_arenas
    def verifica_existencia(self, nome):
        """
        Verifica se já existe uma arena com o nome fornecido.

        Args:
            nome (str): Nome do arena a ser verificado.

        Returns:
            bool: True se já existir, False caso contrário.
        """
        for arena in GerenciamentoArenas._lista_arenas:
            if arena.nome_arena == nome:
                return True
        return False

    def _serializar_arenas(self):
        """
        Converte as arenas em uma string formatada para salvar no arquivo.

        Returns:
            str: Conteúdo de todas as arenas formatado.
        """
        arena_str = ''
        for arena in GerenciamentoArenas._lista_arenas:
            arena_str += f"\n### {arena.nome_arena}\n"
            arena_str += f"- **Mapa**: {arena.mapa.nome_mapa}\n"
            arena_str += f"- **Tipo**: {arena.tipo_jogo}\n"
            arena_str += f"- **Limite Jogadores**: {arena.limite_jogadores}\n"
            arena_str += f"- **Personagens**:\n"
            for personagem in arena.lista_personagens:
                arena_str += f" - {personagem.nome}\n"
            arena_str += '\n'
        return arena_str

    def _reescrever_arquivo(self):
        """
        Sobrescreve o arquivo com o estado atual da lista de arenas.
        """
        with open(self.arquivo, 'w') as file:
            file.write(self._serializar_arenas())

    def salvar_arena(self, nome_arena, tipo, mapa, personagens_arena):
        """
        Cria e salva uma nova arena, se não existir outra com o mesmo nome.

        Args:
            nome_arena (str): Nome da arena.
            tipo (TipoJogo): Tipo de jogo da arena.
            mapa (Mapa): Mapa da arena.
            personagens_arena (list): Lista de personagens atribuídos à arena.
        """
        if any(a.nome_arena == nome_arena for a in self._lista_arenas):
            st.warning(f"Arena '{nome_arena}' já existe.")
            return

        arena = Arena(nome_arena, tipo, mapa)
        for personagem in personagens_arena:
            arena.add_personagens(personagem)
        GerenciamentoArenas._lista_arenas.append(arena)

        with open(self.arquivo, 'a') as file:
            file.write(f"\n### {arena.nome_arena}\n")
            file.write(f"- **Mapa**: {arena.mapa.nome_mapa}\n")
            file.write(f"- **Tipo**: {arena.tipo_jogo}\n")
            file.write(f"- **Limite Jogadores**: {arena.limite_jogadores}\n")
            file.write(f"- **Personagens**:\n")
            for personagem in arena.lista_personagens:
                file.write(f" - {personagem.nome}\n")
            file.write('\n')

    def excluir_arena(self, arena_remove):
        """
        Remove uma arena da lista e atualiza o arquivo.

        Args:
            arena_remove (Arena): Instância da arena a ser removida.
        """
        if arena_remove in GerenciamentoArenas._lista_arenas:
            GerenciamentoArenas._lista_arenas.remove(arena_remove)
            self._reescrever_arquivo()

    def editar_arena(self, arena_editar, nome_arena, tipo, mapa, personagens_arena):
        """
        Substitui uma arena existente por uma nova com as informações atualizadas.

        Args:
            arena_editar (Arena): Arena a ser editada.
            nome_arena (str): Novo nome da arena.
            tipo (TipoJogo): Novo tipo de jogo.
            mapa (Mapa): Novo mapa.
            personagens_arena (list): Nova lista de personagens.
        """
        if arena_editar in GerenciamentoArenas._lista_arenas:
            nova_arena = Arena(nome_arena, tipo, mapa)
            for personagem in personagens_arena:
                nova_arena.add_personagens(personagem)

            index = GerenciamentoArenas._lista_arenas.index(arena_editar)
            GerenciamentoArenas._lista_arenas[index] = nova_arena
            self._reescrever_arquivo()

    def ler_arquivo(self):
        """
        Lê o conteúdo do arquivo de arenas, removendo linhas vazias.

        Returns:
            list: Lista de strings representando cada linha do arquivo.
        """
        with open(self.arquivo, 'r') as entrada:
            entrada = entrada.readlines()
            entrada = [x.strip() for x in entrada if x.strip() != '']
            return entrada

    def ler_arenas(self):
        """
        Lê as arenas do arquivo e as carrega na memória.

        Em caso de erro de leitura ou inconsistência, registra no arquivo 'logs_erro_arenas.txt'.

        Returns:
            list: Lista atualizada de arenas.
        """
        if len(GerenciamentoArenas._lista_arenas) == 0:
            try:
                entrada = self.ler_arquivo()
                i = 0
                while i < len(entrada):
                    try:
                        if entrada[i].startswith('###'):
                            nome = entrada[i].replace('###', '').strip()
                            if any(a.nome_arena == nome for a in self._lista_arenas):
                                i += 1
                                continue

                            i += 1
                            if i < len(entrada) and entrada[i].startswith('- **Mapa**:'):
                                mapa_nome = entrada[i].replace('- **Mapa**:', '').strip()
                                mapa = self.mapas_dict.get(mapa_nome)
                                i += 1

                                if not mapa:
                                    raise ValueError(f"Mapa '{mapa_nome}' não encontrado.")

                                if i < len(entrada) and entrada[i].startswith('- **Tipo**:'):
                                    tipo_nome = entrada[i].replace('- **Tipo**:', '').strip()
                                    tipo = self.tipo_dict.get(tipo_nome)
                                    i += 1

                                    if not tipo:
                                        raise ValueError(f"Tipo '{tipo_nome}' não encontrado.")

                                    if i < len(entrada) and entrada[i].startswith('- **Limite Jogadores**:'):
                                        limite_str = entrada[i].replace('- **Limite Jogadores**:', '').strip()
                                        try:
                                            limite = int(limite_str)
                                        except ValueError:
                                            raise ValueError(f"Limite inválido: {limite_str}")
                                        i += 1

                                        if i < len(entrada) and entrada[i].startswith('- **Personagens**:'):
                                            i += 1
                                            arena = Arena(nome, tipo, mapa)
                                            while i < len(entrada) and entrada[i].startswith('-') and len(arena.lista_personagens) < arena.limite_jogadores:
                                                personagem_nome = entrada[i].replace('-', '').strip()
                                                for personagem in st.session_state.personagens_lidos:
                                                    if personagem.nome == personagem_nome:
                                                        arena.add_personagens(personagem)
                                                i += 1
                                            GerenciamentoArenas._lista_arenas.append(arena)
                                        else:
                                            i += 1
                                    else:
                                        i += 1
                                else:
                                    i += 1
                            else:
                                i += 1
                        else:
                            i += 1
                    except Exception as e:
                        with open("data/logs_erro_arenas.txt", "a", encoding="utf-8") as log_file:
                            log_file.write(f"[Erro na leitura da arena na linha {i}] {str(e)}\n")
                        i += 1
            except Exception as e:
                with open("data/logs_erro_arenas.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"[Erro ao abrir/processar o arquivo '{self.arquivo}']: {str(e)}\n")

        return GerenciamentoArenas._lista_arenas
