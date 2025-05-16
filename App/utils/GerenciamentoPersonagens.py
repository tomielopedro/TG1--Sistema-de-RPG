from RPG import *


class GerenciamentoPersonagens:
    _instance = None
    _lista_personagens = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciamentoPersonagens, cls).__new__(cls)
        return cls._instance

    def __init__(self, arquivo, classes_dict, habilidades_dict):
        # Inicializa apenas uma vez
        if not hasattr(self, '_initialized'):
            self.arquivo = arquivo
            self.classes_dict = classes_dict
            self.habilidades_dict = habilidades_dict
            self._initialized = True  # Impede reconfiguração
            self.ler_personagens()

    @classmethod
    def get_personagens(cls):
        return cls._lista_personagens

    def ler_arquivo(self):
        with open(self.arquivo, 'r') as entrada:
            entrada = entrada.readlines()
            entrada = [x.strip() for x in entrada if x.strip() != '']
            return entrada


    def verifica_existencia(self, nome):
        for personagem in GerenciamentoPersonagens._lista_personagens:
            if personagem.nome == nome:
                return True
        return False


    def salvar_personagem(self, nome, classe, habilidades):
        personagem = Personagem(nome, classe, habilidades)
        GerenciamentoPersonagens._lista_personagens.append(personagem)
        with open(self.arquivo, 'a') as file:
            file.write(f"\n### {personagem.nome}\n")
            file.write(f"- **Classe**: {personagem.classe.nome}\n")
            file.write(f"- **Habilidades**:\n")
            for habilidade in personagem.inventario:
                file.write(f"- {habilidade.nome}\n")  # padroniza com um traço só



    def ler_personagens(self):
        if len(GerenciamentoPersonagens._lista_personagens) == 0:
            entrada = self.ler_arquivo()
            i = 0
            while i < len(entrada):
                if entrada[i].startswith('###'):
                    nome = entrada[i].replace('###', '').strip()
                    i += 1
                    if i < len(entrada) and entrada[i].startswith('- **Classe**:'):
                        classe_nome = entrada[i].replace('- **Classe**:', '').strip()
                        classe = self.classes_dict.get(classe_nome)
                        i += 1
                        if not classe:
                            continue

                        if i < len(entrada) and entrada[i].startswith('- **Habilidades**:'):
                            i += 1
                            habilidades = []
                            while i < len(entrada) and entrada[i].startswith('-') and len(habilidades) < classe.limite_habilidades:
                                habilidade_nome = entrada[i].replace('-', '').strip()
                                habilidade = self.habilidades_dict.get(habilidade_nome)
                                if habilidade:
                                    habilidades.append(habilidade)
                                i += 1

                            personagem = Personagem(nome, classe, habilidades)
                            GerenciamentoPersonagens._lista_personagens.append(personagem)
                else:
                    i += 1
        else:
            return GerenciamentoPersonagens._lista_personagens