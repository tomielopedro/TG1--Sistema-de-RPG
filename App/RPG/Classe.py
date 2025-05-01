from abc import ABC, abstractmethod
from Dados import *


class Classe(ABC):

    def __init__(self, nome: str, pontos_vida: int, dado_ataque: Dados, pontos_ataque: int, pontos_defesa: int, limite_habilidades: int):
        self.nome = nome
        self.pontos_vida = pontos_vida
        self.dado_ataque = dado_ataque
        self.pontos_ataque = pontos_ataque
        self.pontos_defesa = pontos_defesa
        self.limite_habilidades = limite_habilidades

    def __str__(self):
        return f'''
        {self.nome}
        {self.dado_ataque}
        {self.pontos_vida}
        {self.pontos_ataque}
        {self.pontos_defesa}
        {self.limite_habilidades}
        '''


class Guerreiro(Classe):
    def __init__(self, nome: str):
        self.nome = nome
        self.pontos_defesa = 8
        self.pontos_vida = 10+(self.pontos_defesa*5)
        self.dado_ataque = D6()
        self.pontos_ataque = 6
        self.limite_habilidades = 2

        super().__init__(self.nome, self.pontos_vida, self.dado_ataque, self.pontos_ataque, self.pontos_defesa, self.limite_habilidades)


