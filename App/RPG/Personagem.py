from .Classe import *
from .Habilidade import *
from .Dados import *
import copy


class Personagem:
    """
    Classe que representa um personagem jogável no RPG.

    Atributos:
        nome (str): Nome do personagem.
        classe (Classe): Classe do personagem (ex: Guerreiro, Mago, Ladino).
        inventario (list[Habilidade]): Lista de habilidades disponíveis.
        pontos_vida (int): Pontos de vida atuais do personagem.
        pontos_defesa (int): Pontos de defesa do personagem.
        dado_ataque (Dados): Tipo de dado utilizado nos ataques.
        pontos_ataque (int): Valor base de ataque do personagem.

    Atributos de Classe:
        personagens_criados (int): Contador de quantos personagens foram instanciados.

    Métodos:
        __init__(nome, classe, inventario): Inicializa um novo personagem.
        __eq__(other): Compara personagens pelo nome.
        usar_habilidade(): Usa uma habilidade do inventário, se permitido.
        atacar(alvo): Realiza um ataque a outro personagem.
        __str__(): Representação em string detalhada.
        __repr__(): Representação em string simples (nome).
        __copy__(): Cria uma cópia superficial do personagem, preservando atributos relevantes.
    """

    personagens_criados = 0

    def __init__(self, nome: str, classe: Classe, inventario: list[Habilidade]):
        """
        Inicializa um novo personagem com nome, classe e habilidades iniciais.

        Args:
            nome (str): Nome do personagem.
            classe (Classe): Instância de uma classe de personagem.
            inventario (list[Habilidade]): Lista de habilidades iniciais.
        """
        self.nome = nome
        self.classe = classe
        self._inventario = inventario.copy()  # Evita efeitos colaterais
        self._pontos_vida = classe.pontos_vida
        self.pontos_defesa = classe.pontos_defesa
        self.dado_ataque = classe.dado_ataque
        self.pontos_ataque = classe.pontos_ataque
        Personagem.personagens_criados += 1

    @property
    def pontos_vida(self):
        return self._pontos_vida

    @pontos_vida.setter
    def pontos_vida(self, valor):
        self._pontos_vida = max(0, valor)  # impede vida negativa

    @property
    def inventario(self):
        return self._inventario

    @inventario.setter
    def inventario(self, habilidades):
        if not all(isinstance(h, Habilidade) for h in habilidades):
            raise ValueError("O inventário deve conter apenas habilidades.")
        self._inventario = habilidades

    def __eq__(self, other):
        """
        Compara dois personagens com base no nome.

        Args:
            other (Personagem): Outro personagem.

        Returns:
            bool: True se os nomes forem iguais, False caso contrário.
        """
        if isinstance(other, Personagem):
            return self.nome == other.nome
        return False

    def verificar_uso_habilidade(self):
        """
        Usa a primeira habilidade disponível no inventário se um D4 sorteado for maior que 2.

        Returns:
            Habilidade ou bool: A habilidade usada, ou False se não for possível usar.
        """
        if self.inventario and D4().jogar() > 2:
            return self.inventario.pop(0)
        return False

    def atacar(self, alvo: 'Personagem'):
        """
        Realiza um ataque a outro personagem. Tenta usar uma habilidade, caso disponível e sorte favorável.
        Em caso de cura, aplica-se ao próprio personagem.

        Args:
            alvo (Personagem): O personagem que será atacado.

        Returns:
            tuple[int, Optional[Habilidade]]: Dano (ou cura) realizado e habilidade usada (se houver).
        """
        try:
            ataque_total = self.dado_ataque.jogar()
            habilidade_usada = None
            habilidade = self.verificar_uso_habilidade()
            if habilidade:
                habilidade_usada = habilidade
                ataque_total = habilidade.usar()

            if habilidade_usada and habilidade_usada.nome == 'Cura':
                self.pontos_vida += ataque_total
            else:
                alvo.pontos_vida -= ataque_total

            return ataque_total, habilidade_usada
        except Exception as e:
            return 0, None

    def __str__(self):
        """
        Retorna uma representação detalhada do personagem.

        Returns:
            str: Nome, classe e habilidades.
        """
        return f'Nome: {self.nome}\n{self.classe}\nInventário: {self.inventario}'

    def __repr__(self):
        """
        Representa o personagem apenas pelo nome (para listas, logs, etc.).

        Returns:
            str: Nome do personagem.
        """
        return self.nome

    def __copy__(self):
        """
        Cria uma cópia superficial do personagem, preservando atributos e estado de combate.

        Returns:
            Personagem: Cópia do personagem original.
        """
        nova_classe = self.classe
        novo_inventario = [copy.copy(h) for h in self.inventario]
        novo_personagem = Personagem(self.nome, nova_classe, novo_inventario)

        novo_personagem.pontos_vida = self.pontos_vida
        novo_personagem.pontos_defesa = self.pontos_defesa
        novo_personagem.pontos_ataque = self.pontos_ataque
        novo_personagem.dado_ataque = copy.copy(self.dado_ataque)

        return novo_personagem
