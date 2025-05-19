from abc import ABC


class TipoJogo(ABC):
    """
    Classe base abstrata que representa um tipo de jogo em uma arena.

    Atributos:
        nome (str): Nome do tipo de jogo (ex: 'X1', 'PVP').
        limite_jogadores (int): Número máximo de jogadores permitidos nesse tipo de jogo.
        icone (str): Caminho para o ícone que representa visualmente o tipo de jogo.

    Métodos:
        __str__(): Retorna o nome do tipo de jogo.
        __eq__(other): Verifica igualdade com outro objeto com base no nome.
        __hash__(): Permite que instâncias sejam usadas como chaves em dicionários.
        __repr__(): Retorna a representação do tipo de jogo (nome).
    """

    def __init__(self, nome, limite_jogadores, icone):
        """
        Inicializa um novo tipo de jogo.

        Args:
            nome (str): Nome do tipo de jogo.
            limite_jogadores (int): Número máximo de jogadores permitidos.
            icone (str): Caminho do ícone representativo.
        """
        self.nome = nome
        self.limite_jogadores = limite_jogadores
        self.icone = icone

    def __str__(self):
        """
        Retorna o nome do tipo de jogo.

        Returns:
            str: Nome do tipo de jogo.
        """
        return self.nome

    def __eq__(self, other):
        """
        Compara dois tipos de jogo com base no nome.

        Args:
            other (TipoJogo): Outro tipo de jogo.

        Returns:
            bool: True se forem do mesmo tipo, False caso contrário.
        """
        return isinstance(other, TipoJogo) and self.nome == other.nome

    def __hash__(self):
        """
        Permite uso de instâncias como chaves de dicionário.

        Returns:
            int: Hash baseado no nome do tipo de jogo.
        """
        return hash(self.nome)

    def __repr__(self):
        """
        Retorna uma representação do tipo de jogo.

        Returns:
            str: Nome do tipo de jogo.
        """
        return self.nome


class X1(TipoJogo):
    """
    Subclasse de TipoJogo que representa um duelo entre dois jogadores.

    Características:
        - Nome: 'X1'
        - Limite: 2 jogadores
        - Ícone: 'assets/images/x1.png'
    """
    def __init__(self):
        super().__init__('X1', 2, 'assets/images/extras/x1.png')


class PVP(TipoJogo):
    """
    Subclasse de TipoJogo que representa um modo jogador contra jogador em massa.

    Características:
        - Nome: 'PVP'
        - Limite: 100 jogadores
        - Ícone: 'assets/images/pvp.png'
    """
    def __init__(self):
        super().__init__('PVP', 100, 'assets/images/extras/pvp.png')
