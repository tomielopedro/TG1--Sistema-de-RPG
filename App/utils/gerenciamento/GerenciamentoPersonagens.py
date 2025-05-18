from RPG import *


class GerenciamentoPersonagens:
    """
    Classe singleton responsável por gerenciar a leitura, criação e armazenamento de personagens.

    Atributos de Classe:
        _instance (GerenciamentoPersonagens): Instância única da classe (singleton).
        _lista_personagens (List[Personagem]): Lista de todos os personagens gerenciados.

    Atributos de Instância:
        arquivo (str): Caminho do arquivo de onde os personagens serão lidos/salvos.
        classes_dict (dict): Dicionário com as classes disponíveis (ex: {"Guerreiro": Guerreiro()}).
        habilidades_dict (dict): Dicionário com habilidades disponíveis (ex: {"Cura": Cura()}).

    Métodos:
        get_personagens(): Retorna a lista de personagens carregados.
        ler_arquivo(): Lê o conteúdo do arquivo e retorna as linhas válidas.
        verifica_existencia(nome): Verifica se já existe um personagem com o nome fornecido.
        salvar_personagem(nome, classe, habilidades): Cria e salva um novo personagem no arquivo e na memória.
        ler_personagens(): Lê os personagens do arquivo e os carrega em memória. Em caso de erro, salva no log.
    """

    _instance = None
    _lista_personagens = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciamentoPersonagens, cls).__new__(cls)
        return cls._instance

    def __init__(self, arquivo, classes_dict, habilidades_dict):
        """
        Inicializa o gerenciador (apenas uma vez, seguindo padrão singleton).

        Args:
            arquivo (str): Caminho do arquivo de personagens.
            classes_dict (dict): Dicionário de classes disponíveis.
            habilidades_dict (dict): Dicionário de habilidades disponíveis.
        """
        if not hasattr(self, '_initialized'):
            self.arquivo = arquivo
            self.classes_dict = classes_dict
            self.habilidades_dict = habilidades_dict
            self._initialized = True
            self.ler_personagens()

    @classmethod
    def get_personagens(cls):
        """
        Retorna a lista de personagens carregados.

        Returns:
            list: Lista de objetos Personagem.
        """
        return cls._lista_personagens

    def ler_arquivo(self):
        """
        Lê o conteúdo do arquivo de personagens e retorna as linhas não vazias.

        Returns:
            list: Lista de strings representando cada linha válida do arquivo.
        """
        with open(self.arquivo, 'r') as entrada:
            entrada = entrada.readlines()
            entrada = [x.strip() for x in entrada if x.strip() != '']
            return entrada


    def verifica_existencia(self, nome):
        """
        Verifica se já existe um personagem com o nome fornecido.

        Args:
            nome (str): Nome do personagem a ser verificado.

        Returns:
            bool: True se já existir, False caso contrário.
        """
        for personagem in GerenciamentoPersonagens._lista_personagens:
            if personagem.nome == nome:
                return True
        return False

    def _serializar_personagens(self):
        """
        Gera uma string com todos os personagens formatados para escrita em arquivo.

        Returns:
            str: Conteúdo formatado de todos os personagens.
        """
        saida = ''
        for personagem in GerenciamentoPersonagens._lista_personagens:
            saida += f"\n### {personagem.nome}\n"
            saida += f"- **Classe**: {personagem.classe.nome}\n"
            saida += f"- **Habilidades**:\n"
            for habilidade in personagem.inventario:
                saida += f"- {habilidade.nome}\n"
            saida += '\n'
        return saida

    def _reescrever_arquivo(self):
        """
        Reescreve o arquivo de personagens com base na lista atual.
        """
        with open(self.arquivo, 'w', encoding='utf-8') as file:
            file.write(self._serializar_personagens())

    def salvar_personagem(self, nome, classe, habilidades):
        personagem = Personagem(nome, classe, habilidades)
        GerenciamentoPersonagens._lista_personagens.append(personagem)
        with open(self.arquivo, 'a') as file:
            file.write(f"\n### {personagem.nome}\n")
            file.write(f"- **Classe**: {personagem.classe.nome}\n")
            file.write(f"- **Habilidades**:\n")
            for habilidade in personagem.inventario:
                file.write(f"- {habilidade.nome}\n")  # padroniza com um traço só


    def editar_personagem(self, nome_original, nova_classe, novas_habilidades):
        """
        Atualiza os dados de um personagem existente e reescreve o arquivo.

        Args:
            nome_original (str): Nome do personagem a ser editado.
            nova_classe (Classe): Nova classe para o personagem.
            novas_habilidades (list[Habilidade]): Novas habilidades.
        """
        for i, personagem in enumerate(GerenciamentoPersonagens._lista_personagens):
            if personagem.nome == nome_original:
                novo_personagem = Personagem(nome_original, nova_classe, novas_habilidades)
                GerenciamentoPersonagens._lista_personagens[i] = novo_personagem
                self._reescrever_arquivo()
                return


    def excluir_personagem(self, personagem: Personagem):
        """
        Remove o personagem da lista e atualiza o arquivo.

        Args:
            personagem (Personagem): Objeto do personagem a ser removido.
        """
        if personagem in GerenciamentoPersonagens._lista_personagens:
            GerenciamentoPersonagens._lista_personagens.remove(personagem)
            self._reescrever_arquivo()
            print(f"[Info] Personagem '{personagem.nome}' removido com sucesso.")
        else:
            print(f"[Aviso] Personagem '{personagem.nome}' não encontrado.")

    def ler_personagens(self):
        """
        Lê os personagens do arquivo já tratado (sem linhas em branco).

        Regras:
        - Cada personagem inicia com '### Nome'.
        - Deve conter '- **Classe**: ClasseValida'.
        - Depois, '- **Habilidades**:' seguido de até N habilidades prefixadas com '-'.
        - Personagens com nome duplicado são ignorados.
        - Habilidades excedentes são ignoradas e registradas em log.

        Logs:
        - Erros são salvos em 'data/logs_erros.txt' com detalhes por personagem.
        """
        if len(GerenciamentoPersonagens._lista_personagens) > 0:
            return GerenciamentoPersonagens._lista_personagens

        try:
            entrada = self.ler_arquivo()
            total = len(entrada)
            i = 0

            while i < total:
                try:
                    linha = entrada[i]

                    if not linha.startswith("###"):
                        i += 1
                        continue

                    nome = linha.replace("###", "").strip()

                    if self.verifica_existencia(nome):
                        with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                            log.write(f"[{nome}] Erro: nome duplicado — personagem já existente.\n")
                        i += 1
                        continue

                    personagem_valido = True
                    habilidades = []
                    habilidades_excedentes = []

                    i += 1
                    if i >= total or not entrada[i].startswith("- **Classe**:"):
                        with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                            log.write(f"[{nome}] Erro: linha de classe ausente ou mal formatada.\n")
                        personagem_valido = False
                        continue

                    classe_nome = entrada[i].replace("- **Classe**:", "").strip()
                    classe = self.classes_dict.get(classe_nome)
                    if not classe:
                        with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                            log.write(f"[{nome}] Erro: classe '{classe_nome}' não encontrada.\n")
                        personagem_valido = False
                        i += 1
                        continue

                    i += 1
                    if i >= total or not entrada[i].startswith("- **Habilidades**:"):
                        with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                            log.write(f"[{nome}] Erro: seção de habilidades ausente ou mal formatada.\n")
                        personagem_valido = False
                        continue

                    i += 1
                    while i < total and entrada[i].startswith("-"):
                        habilidade_nome = entrada[i].replace("-", "").strip()
                        habilidade = self.habilidades_dict.get(habilidade_nome)

                        if habilidade:
                            if len(habilidades) < classe.limite_habilidades:
                                habilidades.append(habilidade)
                            else:
                                habilidades_excedentes.append(habilidade_nome)
                        else:
                            with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                                log.write(f"[{nome}] Erro: habilidade '{habilidade_nome}' não encontrada.\n")
                        i += 1

                    if habilidades_excedentes:
                        with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                            log.write(
                                f"[{nome}] Aviso: habilidades excedentes ignoradas devido ao limite da classe "
                                f"({classe.limite_habilidades}): {', '.join(habilidades_excedentes)}\n"
                            )

                    if personagem_valido:
                        personagem = Personagem(nome, classe, habilidades)
                        GerenciamentoPersonagens._lista_personagens.append(personagem)

                except Exception as e:
                    with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                        log.write(f"[Erro inesperado] Problema ao processar personagem '{nome}': {str(e)}\n")
                    i += 1

        except Exception as e:
            with open("data/logs_erros.txt", "a", encoding="utf-8") as log:
                log.write(f"[Erro ao abrir/processar o arquivo '{self.arquivo}']: {str(e)}\n")

        return GerenciamentoPersonagens._lista_personagens




