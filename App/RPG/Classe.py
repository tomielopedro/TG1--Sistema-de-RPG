from abc import ABC, abstractmethod
from .Dados import *


class Classe(ABC):

    def __init__(self, nome: str, pontos_vida: int, dado_ataque: Dados, pontos_ataque: int, pontos_defesa: int, limite_habilidades: int, foto: str):
        self.nome = nome
        self.pontos_vida = pontos_vida
        self.dado_ataque = dado_ataque
        self.pontos_ataque = pontos_ataque
        self.pontos_defesa = pontos_defesa
        self.limite_habilidades = limite_habilidades
        self.foto = foto

    def __str__(self):
        return f'Classe: {self.nome}\nPontos de Ataque: {self.pontos_ataque}\nDado de Ataque: {self.dado_ataque}\nPontos de Vida:{self.pontos_vida}\nPontos de Defesa:{self.pontos_defesa}\nLimite de Habilidades:{self.limite_habilidades}'
    def __repr__(self):
        return self.nome


class Guerreiro(Classe):
    def __init__(self):
        self.pontos_defesa = 8  
        self.pontos_vida = 10 + (self.pontos_defesa * 5)
        super().__init__("Guerreiro", self.pontos_vida, D12(), 6, self.pontos_defesa, 2, './assets/images/guerreiro.png')


class Mago(Classe):
    def __init__(self):
        self.pontos_defesa = 3
        self.pontos_vida = 8 + (self.pontos_defesa *2)
        super().__init__("Mago", self.pontos_vida, D6(), 10, self.pontos_defesa, 5, './assets/images/mago.png')


class Ladino(Classe):
    def __init__(self):
        self.pontos_defesa = 5
        self.pontos_vida = 6 + (self.pontos_defesa *3)
        super().__init__("Ladino", self.pontos_vida, D8(), 8, self.pontos_defesa, 2, './assets/images/ladino.png')
 
    
if __name__ == "__main__":
    g1 = Guerreiro()
    print(g1)
    print (f'-'* 20)
    m1 = Mago()
    print(m1)
    print (f'-'* 20)
    l1 = Ladino()
    print(l1)
    print (f'-'* 20)
    