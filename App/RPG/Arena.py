from .Personagem import Personagem
from .Habilidade import *
from .Dados import *

class Arena:
    """
    Classe que representa uma arena de combate onde personagens podem ser adicionados
    e realizar batalhas entre si utilizando habilidades.

    Atributos:
        nome_arena (str): Nome identificador da arena.
        lista_personagens (list): Lista de personagens presentes na arena.
    """

    def __init__(self, nome_arena):
        """
        Inicializa a arena com um nome e uma lista vazia de personagens.

        Parâmetros:
            nome_arena (str): Nome da arena.
        """
        self.nome_arena = nome_arena
        self.lista_personagens = []

    def add_personagens(self, personagem):
        """
        Adiciona um personagem à arena, caso seja uma instância válida da classe Personagem.

        Parâmetros:
            personagem (Personagem): Personagem a ser adicionado à arena.
        """
        if isinstance(personagem, Personagem):
            self.lista_personagens.append(personagem)

    def remove_personagem(self, personagem):
        """
        Remove um personagem da arena, caso seja uma instância válida da classe Personagem.

        Parâmetros:
            personagem (Personagem): Personagem a ser removido da arena.
        """
        if isinstance(personagem, Personagem):
            self.lista_personagens.remove(personagem)

    def combate(self, atacante: Personagem, alvo: Personagem, habilidade_ataque: Habilidade):
        """
        Executa um combate entre dois personagens usando uma habilidade.

        O combate é decidido lançando um dado D20, somando ao poder de ataque do atacante.
        Se o valor for maior que a defesa do alvo, o ataque é bem-sucedido.

        Parâmetros:
            atacante (Personagem): Personagem que realiza o ataque.
            alvo (Personagem): Personagem que será atacado.
            habilidade_ataque (Habilidade): Habilidade utilizada no ataque.

        Retorna:
            bool: True se o ataque foi bem-sucedido, False caso contrário.
        """
        if isinstance(atacante, Personagem) and isinstance(alvo, Personagem) and isinstance(habilidade_ataque, Habilidade):
            if atacante in self.lista_personagens and alvo in self.lista_personagens:
                numero_d20 = D20().jogar()
                dano_ataque = atacante.pontos_ataque + numero_d20
                if dano_ataque > alvo.pontos_defesa:
                    atacante.atacar(alvo, habilidade_ataque)
                    return True
                return False

    def __str__(self):
        """
        Retorna o nome da arena como representação em string.
        """
        return self.nome_arena

    def __repr__(self):
        """
        Retorna o nome da arena como representação formal do objeto.
        """
        return self.nome_arena