from .Classe import *
from .Habilidade import *
from .Dados import *


class Personagem:
    """Classe que representa um personagem do jogo."""

    personagens_criados = 0

    def __init__(self, nome: str, classe: Classe, inventario: list[Habilidade]):
        """
        Inicializa um novo personagem.
        """
        self.nome = nome
        self.classe = classe
        self.inventario = inventario.copy()  # Evita mutabilidade indesejada
        self.pontos_vida = classe.pontos_vida
        self.pontos_defesa = classe.pontos_defesa
        self.dado_ataque = classe.dado_ataque
        self.pontos_ataque = classe.pontos_ataque
        Personagem.personagens_criados += 1

        # Adiciona à lista de personagens criados, se ainda não existir


    def __eq__(self, other):
        """
        Define igualdade de personagens com base no nome.
        """
        if isinstance(other, Personagem):
            return self.nome == other.nome
        return False


    def usar_habilidade(self, habilidade: Habilidade):
        """
        Usa uma habilidade se ela estiver no inventário e o dado permitir.
        Remove a habilidade do inventário após o uso.
        """
        for h in self.inventario:
            if isinstance(h, type(habilidade)) and D4().jogar() > 2:
                print(f'{self.nome} usou a habilidade {h.nome}')
                self.inventario.remove(h)
                return h.usar()
        return 0

    def morrer(self, personagem):
        if isinstance(personagem, Personagem):
            personagem.classe.foto_morte()
            personagem.pontos_vida = 0

    def atacar(self, alvo: 'Personagem', habilidade: Habilidade):
        """
        Realiza ataque a outro personagem usando uma habilidade.
        """
        dano_habilidade = self.usar_habilidade(habilidade)
        ataque_total = dano_habilidade + self.pontos_ataque
        print(f'{alvo.nome}: vida {alvo.pontos_vida}')
        alvo.pontos_vida -= ataque_total
        if alvo.pontos_vida <= 0:
            self.morrer(alvo)
        print(f'{alvo.nome}: vida {alvo.pontos_vida}')

        return ataque_total, dano_habilidade > 0

    def __str__(self):
        return f'Nome: {self.nome}\n{self.classe}\nInventário: {self.inventario}'

    def __repr__(self):
        return self.nome
