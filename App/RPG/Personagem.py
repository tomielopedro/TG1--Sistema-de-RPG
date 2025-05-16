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

    def usar_habilidade(self):
        """
        Usa uma habilidade se estiver no inventário e o dado permitir.
        Remove a habilidade do inventário após o uso.
        Retorna a habilidade usada ou None.
        """
        if self.inventario and D4().jogar() > 2:
            return self.inventario.pop(0)
        return False

    def atacar(self, alvo: 'Personagem'):
        """
        Realiza um ataque contra outro personagem. Tenta usar uma habilidade, se disponível,
        e ajusta os pontos de vida do alvo (ou do próprio personagem, no caso de cura).

        Retorna:
            Tuple[int, Optional[Habilidade]]: Dano (ou cura) causado e habilidade usada (se houver).
        """
        ataque_total = self.dado_ataque.jogar()
        habilidade_usada = None

        # Tenta usar uma habilidade, se houver no inventário
        if len(self.inventario) > 0:
            habilidade = self.usar_habilidade()
            if habilidade:
                habilidade_usada = habilidade
                ataque_total = habilidade.usar()

        # Aplica efeito da habilidade ou do ataque simples
        if habilidade_usada and habilidade_usada.nome == 'Cura':
            self.pontos_vida += ataque_total
        else:
            alvo.pontos_vida -= ataque_total

        return ataque_total, habilidade_usada

    def __str__(self):
        return f'Nome: {self.nome}\n{self.classe}\nInventário: {self.inventario}'

    def __repr__(self):
        return self.nome

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

