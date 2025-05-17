from random import randint


class Dados:

    def __init__(self, numero_lados):
        self.numero_lados = numero_lados

    def __str__(self):
        return f'D{self.numero_lados}'

    def __repr__(self):
        return f'D{self.numero_lados}'

    def __eq__(self, other):
        return self.numero_lados == other.numero_lados

    def jogar(self):
        return randint(1, self.numero_lados)


class D4(Dados):
    def __init__(self):
        super().__init__(4)


class D6(Dados):
    def __init__(self):
        super().__init__(6)


class D8(Dados):
    def __init__(self):
        super().__init__(8)


class D10(Dados):
    def __init__(self):
        super().__init__(10)


class D12(Dados):
    def __init__(self):
        super().__init__(12)


class D20(Dados):
    def __init__(self):
        super().__init__(20)






