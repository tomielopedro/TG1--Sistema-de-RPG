class Habilidade:
    """
    Classe que representa uma habilidade utilizada por um personagem em combate.

    Atributos:
        nome (str): Nome da habilidade.
        descricao (str): Descrição textual do efeito da habilidade.
        pontos_ataque (int): Pontos de ataque causados pela habilidade.
        foto_habilidade (str): Caminho para a imagem representativa da habilidade.

    Métodos:
        usar(): Retorna os pontos de ataque da habilidade.
        __str__(): Retorna uma descrição legível da habilidade.
        __repr__(): Retorna o nome da habilidade.
    """

    def __init__(self, nome: str, descricao: str, pontos_ataque: int, foto_habilidade):
        """
        Inicializa uma nova habilidade com nome, descrição, pontos de ataque e imagem.

        Args:
            nome (str): Nome da habilidade.
            descricao (str): Descrição da habilidade.
            pontos_ataque (int): Valor de ataque causado pela habilidade.
            foto_habilidade (str): Caminho da imagem da habilidade.
        """
        self.nome = nome
        self.descricao = descricao
        self.pontos_ataque = pontos_ataque
        self.foto_habilidade = foto_habilidade

    def usar(self):
        """
        Utiliza a habilidade e retorna o valor de ataque.

        Returns:
            int: Pontos de ataque da habilidade.
        """
        return self.pontos_ataque

    def __str__(self):
        """
        Retorna uma representação em string legível da habilidade.

        Returns:
            str: String formatada com os dados da habilidade.
        """
        return f'Nome: {self.nome} - Descricao: {self.descricao} - Pontos ataque: {self.pontos_ataque}'

    def __repr__(self):
        """
        Retorna uma representação reduzida da habilidade (somente o nome).

        Returns:
            str: Nome da habilidade.
        """
        return self.nome


class BolaDeFogo(Habilidade):
    """
    Subclasse de Habilidade que representa uma bola de fogo.

    Características:
        - Causa 10 pontos de dano em área.
        - Tem imagem associada em './assets/images/bola_fogo.png'.
    """
    def __init__(self):
        super().__init__('BolaDeFogo', 'Uma bola de fogo que causa dano em área', 10, './assets/images/habilidades/bola_fogo.png')


class Cura(Habilidade):
    """
    Subclasse de Habilidade que representa uma cura.

    Características:
        - Restaura 10 pontos de vida.
        - Tem imagem associada em './assets/images/cura.png'.
    """
    def __init__(self):
        super().__init__('Cura', 'Se curou usando uma dose de elixir da vida', 10, './assets/images/habilidades/cura.png')


class TiroDeArco(Habilidade):
    """
    Subclasse de Habilidade que representa um tiro de arco.

    Características:
        - Causa 6 pontos de dano.
        - Tem imagem associada em './assets/images/arco.png'.
    """
    def __init__(self):
        super().__init__('TiroDeArco', 'Um tiro de arco que causa dano em área', 6, './assets/images/habilidades/arco.png')

