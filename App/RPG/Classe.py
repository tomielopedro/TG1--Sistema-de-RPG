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
    def __init__(self):
        self.pontos_vida = 10 + (self.pontos_defesa *5)
        self.pontos_defesa = 8  
        super().__init__("Guerreiro", self.pontos_vida, D12(), 6, self.pontos_defesa, 2)

class Mago(Classe):
    def __init__(self):
        self.pontos_vida = 8 + (self.pontos_defesa *2)
        self.pontos_defesa
        super().__init__("Mago", self.pontos_vida, D6(), 10, self.pontos_defesa, 5)
        
class Ladino(Classe):
    def __init__(self):
        self.pontos_vida = 6 + (self.pontos_defesa *3)
        self.pontos_defesa = 5
        super().__init__("Ladino", self.pontos_vida, D8(), 8, self.pontos_defesa, 2)
 
    
m1 = Mago()