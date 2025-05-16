from abc import ABC

class Mapa(ABC):
    def __init__(self, nome_mapa, foto_mapa):
        self.nome_mapa = nome_mapa
        self.foto_mapa = foto_mapa

    def __str__(self):
        return self.nome_mapa

    def __repr__(self):
        return self.nome_mapa

    def __eq__(self, other):
        return isinstance(other, Mapa) and self.nome_mapa == other.nome_mapa

    def __hash__(self):
        return hash(self.nome_mapa)

class Winter(Mapa):
    def __init__(self):
        super().__init__('Winter', './assets/images/maps/winter.png')




class Castle(Mapa):
    def __init__(self):
        super().__init__('Castle', './assets/images/maps/castle.png')