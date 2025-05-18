from abc import ABC, abstractmethod
from .Dados import *

class Classe(ABC):
    """
    Classe abstrata que define o modelo base para classes de personagens em um jogo RPG.

    Atributos:
        nome (str): Nome da classe (ex: Guerreiro, Mago), relaciona-se ao tipo do personagem.
        pontos_vida (int): Quantidade de vida total da classe.
        dado_ataque (Dados): Tipo de dado utilizado para calcular o dano de ataque.
        pontos_ataque (int): Valor base de ataque da classe.
        pontos_defesa (int): Valor base de defesa da classe.
        limite_habilidades (int): Número Limite de habilidades que um personagem dessa classe pode ter.
        foto (str): Caminho para a imagem representando a classe.

    Métodos:
        __str__(): Retorna uma representação legível da classe com suas estatísticas.
        __repr__(): Retorna o nome da classe.
    """

    def __init__(self, nome: str, pontos_vida: int, dado_ataque: Dados,
                 pontos_ataque: int, pontos_defesa: int, limite_habilidades: int, foto: str):
        self.nome = nome
        self._pontos_vida = pontos_vida
        self.dado_ataque = dado_ataque
        self.pontos_ataque = pontos_ataque
        self.pontos_defesa = pontos_defesa
        self.limite_habilidades = limite_habilidades
        self.foto = foto

    @property
    def pontos_vida(self):
        return self._pontos_vida

    @pontos_vida.setter
    def pontos_vida(self, valor):
        if valor < 0:
            raise ValueError("Vida não pode ser negativa.")
        self._pontos_vida = valor
    def __str__(self):
        """
        Retorna uma string referente às estatísticas da classe.

        Returns:
            str: Representação formatada da classe.
        """
        return (f'Classe: {self.nome}\n'
                f'Pontos de Ataque: {self.pontos_ataque}\n'
                f'Dado de Ataque: {self.dado_ataque}\n'
                f'Pontos de Vida: {self.pontos_vida}\n'
                f'Pontos de Defesa: {self.pontos_defesa}\n'
                f'Limite de Habilidades: {self.limite_habilidades}')

    def __repr__(self):
        """
        Retorna o nome da classe.

        Returns:
            str: Nome da classe.
        """
        return self.nome


class Guerreiro(Classe):
    """
    Classe concreta que representa o Guerreiro.

    Características:
        - Alta defesa (8).
        - Vida: 10 + (defesa * 5).
        - Ataque moderado (6) 
        - Dado D12.
        - Limite de habilidades (2).
    """
    def __init__(self):
        self.pontos_defesa = 8
        self.pontos_vida = 10 + (self.pontos_defesa * 5)
        super().__init__("Guerreiro", self.pontos_vida, D12(), 6, self.pontos_defesa, 2, 'assets/images/personagens/guerreiro.png')


class Mago(Classe):
    """
    Classe concreta que representa o Mago.

    Características:
        - Baixa defesa (3).
        - Vida: 8 + (defesa * 2).
        - Alto ataque (10) 
        - Dado D6.
        - Limite de habilidades (5).
    """
    def __init__(self):
        self.pontos_defesa = 3
        self.pontos_vida = 8 + (self.pontos_defesa * 2)
        super().__init__("Mago", self.pontos_vida, D6(), 10, self.pontos_defesa, 5, 'assets/images/personagens/mago.png')


class Ladino(Classe):
    """
    Classe concreta que representa o Ladino.

    Características:
        - Defesa média (5).
        - Vida: 6 + (defesa * 3).
        - Ataque ágil (8)
        - Dado D8.
        - Limite de habilidades (2).
    """
    def __init__(self):
        self.pontos_defesa = 5
        self.pontos_vida = 6 + (self.pontos_defesa * 3)
        super().__init__("Ladino", self.pontos_vida, D8(), 8, self.pontos_defesa, 2, 'assets/images/personagens/ladino.png')
