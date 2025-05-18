from RPG import *
import streamlit as st
from datetime import datetime

class GerenciamentoArenas:
    _instance = None
    _lista_arenas = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciamentoArenas, cls).__new__(cls)
        return cls._instance

    def __init__(self, arquivo, mapas_dict, tipo_dict):
        if not hasattr(self, '_initialized'):
            self.arquivo = arquivo
            self.mapas_dict = mapas_dict
            self.tipo_dict = tipo_dict
            self._initialized = True
            self.ler_arenas()

    @classmethod
    def get_arenas(cls):
        return cls._lista_arenas

    def verifica_existencia(self, nome):
        return any(arena.nome_arena == nome for arena in self._lista_arenas)

    def _serializar_arenas(self):
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
        with open(self.arquivo, 'w') as file:
            file.write(self._serializar_arenas())

    def salvar_arena(self, nome_arena, tipo, mapa, personagens_arena):
        if any(a.nome_arena == nome_arena for a in self._lista_arenas):
            st.warning(f"Arena '{nome_arena}' já existe.")
            self.escrever_log(nome_arena, "Aviso", "tentativa de criação de arena com nome duplicado.")
            return

        arena = Arena(nome_arena, tipo, mapa)
        for personagem in personagens_arena:
            arena.add_personagens(personagem)
        self._lista_arenas.append(arena)

        with open(self.arquivo, 'a') as file:
            file.write(f"\n### {arena.nome_arena}\n")
            file.write(f"- **Mapa**: {arena.mapa.nome_mapa}\n")
            file.write(f"- **Tipo**: {arena.tipo_jogo}\n")
            file.write(f"- **Limite Jogadores**: {arena.limite_jogadores}\n")
            file.write(f"- **Personagens**:\n")
            for personagem in arena.lista_personagens:
                file.write(f" - {personagem.nome}\n")
            file.write('\n')

        # LOG de criação
        self.escrever_log(nome_arena, "Info", "arena criada com sucesso.")

    def editar_arena(self, arena_editar, nome_arena, tipo, mapa, personagens_arena):
        if arena_editar in self._lista_arenas:
            nova_arena = Arena(nome_arena, tipo, mapa)
            for personagem in personagens_arena:
                nova_arena.add_personagens(personagem)

            index = self._lista_arenas.index(arena_editar)
            self._lista_arenas[index] = nova_arena
            self._reescrever_arquivo()
            self.escrever_log(nome_arena, "Info", "arena editada com sucesso.")

    def excluir_arena(self, arena_remove):
        if arena_remove in self._lista_arenas:
            self._lista_arenas.remove(arena_remove)
            self._reescrever_arquivo()
            self.escrever_log(arena_remove.nome_arena, "Info", "arena excluída com sucesso.")
        else:
            self.escrever_log(arena_remove.nome_arena, "Aviso", "tentativa de exclusão de arena inexistente.")

    def escrever_log(self, nome, tipo, mensagem):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data/logs_arena.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] [{nome}] {tipo}: {mensagem}\n")

    def ler_arquivo(self):
        with open(self.arquivo, 'r') as entrada:
            return [x.strip() for x in entrada.readlines() if x.strip()]

    def ler_arenas(self):
        if len(self._lista_arenas) == 0:
            try:
                entrada = self.ler_arquivo()
                i = 0
                while i < len(entrada):
                    try:
                        if entrada[i].startswith('###'):
                            nome = entrada[i].replace('###', '').strip()
                            if self.verifica_existencia(nome):
                                i += 1
                                continue

                            i += 1
                            mapa_nome = entrada[i].replace('- **Mapa**:', '').strip()
                            mapa = self.mapas_dict.get(mapa_nome)
                            if not mapa:
                                raise ValueError(f"Mapa '{mapa_nome}' não encontrado.")
                            i += 1

                            tipo_nome = entrada[i].replace('- **Tipo**:', '').strip()
                            tipo = self.tipo_dict.get(tipo_nome)
                            if not tipo:
                                raise ValueError(f"Tipo '{tipo_nome}' não encontrado.")
                            i += 1

                            limite_str = entrada[i].replace('- **Limite Jogadores**:', '').strip()
                            try:
                                limite = int(limite_str)
                            except ValueError:
                                raise ValueError(f"Limite inválido: {limite_str}")
                            i += 1

                            if not entrada[i].startswith('- **Personagens**:'):
                                raise ValueError("Seção de personagens ausente ou mal formatada.")
                            i += 1

                            arena = Arena(nome, tipo, mapa)
                            while i < len(entrada) and entrada[i].startswith('-') and len(arena.lista_personagens) < limite:
                                personagem_nome = entrada[i].replace('-', '').strip()
                                for personagem in st.session_state.personagens_lidos:
                                    if personagem.nome == personagem_nome:
                                        arena.add_personagens(personagem)
                                i += 1

                            self._lista_arenas.append(arena)
                        else:
                            i += 1

                    except Exception as e:
                        self.escrever_log(nome, "Erro", f"na leitura da arena na linha {i}: {str(e)}")
                        i += 1

            except Exception as e:
                self.escrever_log("Sistema", "Erro crítico", f"ao abrir/processar o arquivo '{self.arquivo}': {str(e)}")

        return self._lista_arenas
