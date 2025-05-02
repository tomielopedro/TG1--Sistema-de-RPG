from .Classe import *
from .Habilidade import *
from .Dados import *


class Personagem:
    """Classe que representa um personagem do jogo."""
    qtd_instancias = 0

    def __init__(self, nome: str, classe: Classe, inventario: list):
        self.nome = nome
        self.classe = classe
        self.inventario = inventario
        self.pontos_vida = classe.pontos_vida
        self.pontos_defesa = classe.pontos_defesa
        self.dado_ataque: classe.dado_ataque
        self.pontos_ataque = classe.pontos_ataque
        Personagem.qtd_instancias += 1

    def usar_habilidade(self, habilidade):
        for h in self.inventario:
            if len(self.inventario) > 0 and isinstance(h, type(habilidade)) and Dados.D4().jogar() > 2:
                print('Usou habilidade')
                self.inventario.remove(h)
                return habilidade.usar()
        return 0

    def atacar(self, alvo, habilidade):
        ataque = self.usar_habilidade(habilidade) + self.pontos_ataque
        alvo.pontos_vida -= ataque
        return ataque

    def __str__(self):
        return f'Nome: {self.nome}\n{self.classe}\nInventario: {self.inventario}'

    def __repr__(self):
        return self.nome

