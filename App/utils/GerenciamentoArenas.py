from RPG import *
import streamlit as st


class GerenciamentoArenas:
    _instance = None
    _lista_arenas = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciamentoArenas, cls).__new__(cls)
        return cls._instance

    def __init__(self, arquivo, mapas_dict, tipo_dict):
        # Inicializa apenas uma vez
        if not hasattr(self, '_initialized'):
            self.arquivo = arquivo
            self._initialized = True  # Impede reconfiguração
            self.mapas_dict = mapas_dict
            self.tipo_dict = tipo_dict
            self.ler_arenas()

    def ler_arquivo(self):
        with open(self.arquivo, 'r') as entrada:
            entrada = entrada.readlines()
            entrada = [x.strip() for x in entrada if x.strip() != '']
            return entrada

    @classmethod
    def get_arenas(cls):
        return cls._lista_arenas

    def _serializar_arenas(self):
        """Gera o conteúdo textual de todas as arenas para escrita em arquivo."""
        arena_str = ''
        for arena in GerenciamentoArenas._lista_arenas:
            arena_str += f"\n### {arena.nome_arena}\n"
            arena_str += f"- **Mapa**: {arena.mapa}\n"
            arena_str += f"- **Tipo**: {arena.tipo_jogo}\n"
            arena_str += f"- **Limite Jogadores**: {arena.limite_jogadores}\n"
            arena_str += f"- **Personagens**:\n"
            for personagem in arena.lista_personagens:
                arena_str += f" - {personagem.nome}\n"
            arena_str += '\n'
        return arena_str

    def _reescrever_arquivo(self):
        """Sobrescreve o arquivo com todas as arenas atuais."""
        with open(self.arquivo, 'w') as file:
            file.write(self._serializar_arenas())

    def salvar_arena(self, nome_arena, tipo, mapa, personagens_arena):
        arena = Arena(nome_arena, tipo, mapa)
        for personagem in personagens_arena:
            arena.add_personagens(personagem)
        GerenciamentoArenas._lista_arenas.append(arena)

        # Adiciona apenas a nova arena no final do arquivo
        with open(self.arquivo, 'a') as file:
            file.write(f"\n### {arena.nome_arena}\n")
            file.write(f"- **Mapa**: {arena.mapa}\n")
            file.write(f"- **Tipo**: {arena.tipo_jogo}\n")
            file.write(f"- **Limite Jogadores**: {arena.limite_jogadores}\n")
            file.write(f"- **Personagens**:\n")
            for personagem in arena.lista_personagens:
                file.write(f" - {personagem.nome}\n")
            file.write('\n')

    def excluir_arena(self, arena_remove):
        if arena_remove in GerenciamentoArenas._lista_arenas:
            GerenciamentoArenas._lista_arenas.remove(arena_remove)
            self._reescrever_arquivo()

    def editar_arena(self, arena_editar, nome_arena, tipo, mapa, personagens_arena):
        if arena_editar in GerenciamentoArenas._lista_arenas:
            nova_arena = Arena(nome_arena, tipo, mapa)
            for personagem in personagens_arena:
                nova_arena.add_personagens(personagem)

            index = GerenciamentoArenas._lista_arenas.index(arena_editar)
            GerenciamentoArenas._lista_arenas[index] = nova_arena
            self._reescrever_arquivo()

    def ler_arenas(self):
        if len(GerenciamentoArenas._lista_arenas) == 0:
            print('entrou aqui')
            entrada = self.ler_arquivo()
            i = 0
            while i < len(entrada):
                if entrada[i].startswith('###'):
                    nome = entrada[i].replace('###', '').strip()

                    i += 1

                    if i < len(entrada) and entrada[i].startswith('- **Mapa**:'):
                        mapa_nome = entrada[i].replace('- **Mapa**:', '').strip()
                        mapa = self.mapas_dict.get(mapa_nome)
                        i += 1

                        if not mapa:
                            continue

                        if i < len(entrada) and entrada[i].startswith('- **Tipo**:'):
                            tipo_nome = entrada[i].replace('- **Tipo**:', '').strip()
                            tipo = self.tipo_dict.get(tipo_nome)
                            i += 1
                            if not tipo:
                                continue

                            if i < len(entrada) and entrada[i].startswith('- **Limite Jogadores**:'):
                                limite_str = entrada[i].replace('- **Limite Jogadores**:', '').strip()
                                try:
                                    limite = int(limite_str)
                                except ValueError:
                                    i += 1
                                    continue
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
        return GerenciamentoArenas._lista_arenas


