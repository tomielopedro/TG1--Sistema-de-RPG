class Habilidade:

    """Classe que representa um habilidade do personagem"""
    def __init__(self, nome: str, descricao: str, pontos_ataque: int):
        self.nome = nome
        self.descricao = descricao
        self.pontos_ataque = pontos_ataque

    def __str__(self):
        return f'''
        Nome: {self.nome}
        Descricao: {self.descricao}
        Pontos ataque: {self.pontos_ataque}
        '''

    def __repr__(self):
        return f'''
        {self.nome}
        {self.descricao}
        {self.pontos_ataque}
        '''


