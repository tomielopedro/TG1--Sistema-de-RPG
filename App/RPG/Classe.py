from abc import ABC, abstractmethod
from Dados import Dados


class Classe(ABC):

    def __init__(self, nome: str, pontos_vida: int, dado_ataque: Dados, pontos_ataque: int, pontos_defesa: int, limite_habilidades: int):
        self.nome = nome
        self.pontos_vida = pontos_vida
        self.dado_ataque = dado_ataque
        self.pontos_ataque = pontos_ataque
        self.pontos_defesa = pontos_defesa
        self.limite_habilidades = limite_habilidades
