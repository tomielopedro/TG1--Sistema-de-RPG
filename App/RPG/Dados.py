from random import randint

class Dados:
    """
    Representa um dado genérico com um número arbitrário de lados.

    Atributos:
        numero_lados (int): Número de lados do dado.

    Métodos:
        __str__(): Retorna uma representação amigável do dado como string.
        __repr__(): Retorna a representação oficial do dado.
        __eq__(other): Verifica se dois dados têm o mesmo número de lados.
        jogar(): Retorna um valor aleatório entre 1 e o número de lados.
    """

    def __init__(self, numero_lados):
        """
        Inicializa um novo dado com o número especificado de lados.

        Args:
            numero_lados (int): Número de lados do dado.
        """
        self.numero_lados = numero_lados

    def __str__(self):
        """Retorna a representação amigável do dado, no formato Dx."""
        return f'D{self.numero_lados}'

    def __repr__(self):
        """Retorna a representação oficial do dado, no formato Dx."""
        return f'D{self.numero_lados}'

    def __eq__(self, other):
        """
        Compara dois dados para verificar se possuem o mesmo número de lados.

        Args:
            other (Dados): Outro objeto da classe Dados.

        Returns:
            bool: True se os dois dados tiverem o mesmo número de lados, False caso contrário.
        """
        return self.numero_lados == other.numero_lados

    def jogar(self):
        """
        Simula o lançamento do dado.

        Returns:
            int: Valor aleatório entre 1 e o número de lados.
        """
        return randint(1, self.numero_lados)


class D4(Dados):
    """Representa um dado de 4 lados (D4)."""
    def __init__(self):
        super().__init__(4)


class D6(Dados):
    """Representa um dado de 6 lados (D6)."""
    def __init__(self):
        super().__init__(6)


class D8(Dados):
    """Representa um dado de 8 lados (D8)."""
    def __init__(self):
        super().__init__(8)


class D10(Dados):
    """Representa um dado de 10 lados (D10)."""
    def __init__(self):
        super().__init__(10)


class D12(Dados):
    """Representa um dado de 12 lados (D12)."""
    def __init__(self):
        super().__init__(12)


class D20(Dados):
    """Representa um dado de 20 lados (D20)."""
    def __init__(self):
        super().__init__(20)
