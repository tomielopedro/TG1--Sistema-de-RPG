from RPG import *
from datetime import datetime


class GerenciamentoPersonagens:
    """
    Classe singleton responsável por gerenciar a leitura, criação, edição, exclusão
    e persistência de personagens em um arquivo de texto.
    """

    _instance = None
    _lista_personagens = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciamentoPersonagens, cls).__new__(cls)
        return cls._instance

    def __init__(self, arquivo, classes_dict, habilidades_dict):
        if not hasattr(self, '_initialized'):
            self.arquivo = arquivo
            self.classes_dict = classes_dict
            self.habilidades_dict = habilidades_dict
            self._initialized = True
            self.ler_personagens()

    @classmethod
    def get_personagens(cls):
        """Retorna a lista atual de personagens carregados."""
        return cls._lista_personagens

    def ler_arquivo(self):
        """Lê o conteúdo do arquivo de personagens, ignorando linhas vazias."""
        with open(self.arquivo, 'r') as entrada:
            return [x.strip() for x in entrada if x.strip() != '']

    def verifica_existencia(self, nome):
        """Verifica se já existe um personagem com o nome fornecido."""
        return any(p.nome == nome for p in GerenciamentoPersonagens._lista_personagens)

    def _serializar_personagens(self):
        """Retorna todos os personagens em formato de string para escrita em arquivo."""
        saida = ''
        for personagem in GerenciamentoPersonagens._lista_personagens:
            saida += f"\n### {personagem.nome}\n"
            saida += f"- **Classe**: {personagem.classe.nome}\n"
            saida += f"- **Habilidades**:\n"
            for habilidade in personagem.inventario:
                saida += f"- {habilidade.nome}\n"
        return saida

    def _reescrever_arquivo(self):
        """Sobrescreve o arquivo com os personagens atuais da lista."""
        with open(self.arquivo, 'w', encoding='utf-8') as file:
            file.write(self._serializar_personagens())

    def salvar_personagem(self, nome, classe, habilidades):
        """
        Salva um novo personagem no arquivo, se não for duplicado.
        """
        if self.verifica_existencia(nome):
            self.escrever_log(nome, "Aviso", "personagem não salvo — nome duplicado.")
            return

        personagem = Personagem(nome, classe, habilidades)
        GerenciamentoPersonagens._lista_personagens.append(personagem)
        with open(self.arquivo, 'a') as file:
            file.write(f"\n### {personagem.nome}\n")
            file.write(f"- **Classe**: {personagem.classe.nome}\n")
            file.write(f"- **Habilidades**:\n")
            for habilidade in personagem.inventario:
                file.write(f"- {habilidade.nome}\n")
        self.escrever_log(nome, "Info", "personagem criado com sucesso.")

    def editar_personagem(self, nome_original, nova_classe, novas_habilidades):
        """Edita um personagem existente com novos dados."""
        for i, personagem in enumerate(GerenciamentoPersonagens._lista_personagens):
            if personagem.nome == nome_original:
                novo_personagem = Personagem(nome_original, nova_classe, novas_habilidades)
                GerenciamentoPersonagens._lista_personagens[i] = novo_personagem
                self._reescrever_arquivo()
                self.escrever_log(nome_original, "Info", "personagem editado com sucesso.")
                return

    def excluir_personagem(self, personagem: Personagem):
        """Exclui um personagem da lista e atualiza o arquivo."""
        if personagem in GerenciamentoPersonagens._lista_personagens:
            GerenciamentoPersonagens._lista_personagens.remove(personagem)
            self._reescrever_arquivo()
            self.escrever_log(personagem.nome, "Info", "personagem excluído com sucesso.")
        else:
            self.escrever_log(personagem.nome, "Aviso", "tentativa de exclusão de personagem inexistente.")

    def escrever_log(self, nome, tipo, mensagem):
        """Registra logs com data/hora, nome, tipo e mensagem."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data/logs_personagem.txt", "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}] [{nome}] {tipo}: {mensagem}\n")

    def parse_bloco_personagem(self, linhas):
        """
        Faz o parsing de um bloco de personagem e retorna um objeto Personagem
        ou None em caso de erro. Também registra os logs.
        """
        try:
            nome = linhas[0].replace("###", "").strip()

            if self.verifica_existencia(nome):
                self.escrever_log(nome, "Aviso", "nome duplicado — personagem já existente.")
                return None

            if not linhas[1].startswith("- **Classe**:"):
                self.escrever_log(nome, "Erro", "linha de classe ausente ou mal formatada.")
                return None

            classe_nome = linhas[1].replace("- **Classe**:", "").strip()
            classe = self.classes_dict.get(classe_nome)
            if not classe:
                self.escrever_log(nome, "Erro", f"classe '{classe_nome}' não encontrada.")
                return None

            if not linhas[2].startswith("- **Habilidades**:"):
                self.escrever_log(nome, "Erro", "seção de habilidades ausente ou mal formatada.")
                return None

            habilidades = []
            habilidades_excedentes = []

            for linha in linhas[3:]:
                if not linha.startswith("-"):
                    continue
                habilidade_nome = linha.replace("-", "").strip()
                if habilidade_nome.lower() == "tiro de arco":
                    habilidade_nome = "TiroDeArco"
                habilidade = self.habilidades_dict.get(habilidade_nome)
                if habilidade:
                    if len(habilidades) < classe.limite_habilidades:
                        habilidades.append(habilidade)
                    else:
                        habilidades_excedentes.append(habilidade_nome)
                else:
                    self.escrever_log(nome, "Erro", f"habilidade '{habilidade_nome}' não encontrada.")

            if habilidades_excedentes:
                self.escrever_log(
                    nome, "Aviso",
                    f"habilidades excedentes ignoradas: {', '.join(habilidades_excedentes)}"
                )

            return Personagem(nome, classe, habilidades)

        except Exception as e:
            self.escrever_log("Parser", "Erro inesperado", f"Falha ao processar personagem: {str(e)}")
            return None

    def importar_adicionando_personagens(self, uploaded_file):
        """
        Importa personagens de um arquivo via upload, usando o parser reutilizável.
        """
        novos_dados = uploaded_file.read().decode("utf-8").splitlines()
        novos_dados = [linha.strip() for linha in novos_dados if linha.strip()]
        bloco = []

        for linha in novos_dados:
            if linha.startswith("###") and bloco:
                personagem = self.parse_bloco_personagem(bloco)
                if personagem:
                    self.salvar_personagem(personagem.nome, personagem.classe, personagem.inventario)
                bloco = [linha]
            else:
                bloco.append(linha)

        if bloco:
            personagem = self.parse_bloco_personagem(bloco)
            if personagem:
                self.salvar_personagem(personagem.nome, personagem.classe, personagem.inventario)

    def ler_personagens(self):
        """Lê todos os personagens do arquivo base e os adiciona na memória."""
        if GerenciamentoPersonagens._lista_personagens:
            return GerenciamentoPersonagens._lista_personagens

        try:
            linhas = self.ler_arquivo()
            bloco = []

            for linha in linhas:
                if linha.startswith("###") and bloco:
                    personagem = self.parse_bloco_personagem(bloco)
                    if personagem:
                        GerenciamentoPersonagens._lista_personagens.append(personagem)
                    bloco = [linha]
                else:
                    bloco.append(linha)

            if bloco:
                personagem = self.parse_bloco_personagem(bloco)
                if personagem:
                    GerenciamentoPersonagens._lista_personagens.append(personagem)

        except Exception as e:
            self.escrever_log("Sistema", "Erro crítico", f"Erro ao abrir/processar o arquivo '{self.arquivo}': {str(e)}")

        return GerenciamentoPersonagens._lista_personagens