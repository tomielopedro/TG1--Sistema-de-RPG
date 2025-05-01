class Habilidade:

    """Classe que representa um habilidade do personagem"""
    def __init__(self, nome: str, descricao: str, pontos_ataque: int):
        self.nome = nome
        self.descricao = descricao
        self.pontos_ataque = pontos_ataque

    def usar(self):
        return f'Habilidade: {self.nome} usada'

    def __str__(self):
        return f'Nome: {self.nome} - Descricao: {self.descricao} - Pontos ataque: {self.pontos_ataque}'

    def __repr__(self):
        return f'{self.nome} {self.descricao} {self.pontos_ataque}'


class BolaDeFogo(Habilidade):

    """Subclasse de Habilidade que representa uma bola de fogo"""
    def __init__(self):
        super().__init__('Bola de Fogo', 'Uma bola de fogo que causa dano em área', -10)


class Cura(Habilidade):
    """Subclasse de Habilidade que representa uma cura"""
    def __init__(self):
        super().__init__('Cura', 'Uma cura que recupera 10 pontos de vida', 10)


class TiroDeArco(Habilidade):
    """Subclasse de Habilidade que representa um tiro de arco"""
    def __init__(self):
        super().__init__('Tiro de Arco', 'Um tiro de arco que causa dano em área', -6)


if __name__ == '__main__':
    print(BolaDeFogo())
    print(Cura())
    print(TiroDeArco())

