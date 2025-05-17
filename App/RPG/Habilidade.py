class Habilidade:

    """Classe que representa um habilidade do personagem"""
    def __init__(self, nome: str, descricao: str, pontos_ataque: int, foto_habilidade):
        self.nome = nome
        self.descricao = descricao
        self.pontos_ataque = pontos_ataque
        self.foto_habilidade = foto_habilidade

    def usar(self):
        return self.pontos_ataque

    def __str__(self):
        return f'Nome: {self.nome} - Descricao: {self.descricao} - Pontos ataque: {self.pontos_ataque}'

    def __repr__(self):
        return self.nome




class BolaDeFogo(Habilidade):

    """Subclasse de Habilidade que representa uma bola de fogo"""
    def __init__(self):
        super().__init__('BolaDeFogo', 'Uma bola de fogo que causa dano em área', 10, './assets/images/bola_fogo.png')


class Cura(Habilidade):
    """Subclasse de Habilidade que representa uma cura"""

    def __init__(self):
        super().__init__('Cura', 'Se curou usando uma dose de elixir da vida', 10, './assets/images/cura.png')


class TiroDeArco(Habilidade):
    """Subclasse de Habilidade que representa um tiro de arco"""
    def __init__(self):
        super().__init__('TiroDeArco', 'Um tiro de arco que causa dano em área', 6, './assets/images/arco.png')


if __name__ == '__main__':
    print(BolaDeFogo())
    print(Cura())
    print(TiroDeArco())

