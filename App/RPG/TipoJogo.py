from abc import ABC


class TipoJogo(ABC):
    def __init__(self, nome, limite_jogadores, icone):

        self.nome = nome
        self.limite_jogadores = limite_jogadores
        self.icone = icone

    def __str__(self):
        return self.nome

    def __eq__(self, other):
        return isinstance(other, TipoJogo) and self.nome == other.nome


    def __hash__(self):
        return hash(self.nome)


    def __repr__(self):

        return self.nome


class X1(TipoJogo):
    def __init__(self):
        super().__init__('X1', 2, './assets/images/x1.png')


class PVP(TipoJogo):
    def __init__(self):
        super().__init__('PVP', 100, './assets/images/pvp.png')