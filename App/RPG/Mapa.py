from abc import ABC
from PIL import Image
import os


class Mapa(ABC):
    """
    Classe abstrata que representa um MAPA onde as BATALHAS ocorrem em uma ARENA.

    Atributos:
        nome_mapa (str): Nome identificador do mapa (ex: "Vilarejo", "Torre").
        foto_mapa (str): Caminho para a imagem associada ao mapa.

    Métodos:
        __str__(): Retorna o nome do mapa como string.
        __repr__(): Representa o mapa como string (para debug ou logs).
        __eq__(other): Compara dois mapas com base no nome.
        __hash__(): Permite usar mapas como chaves em dicionários ou em conjuntos.
    """

    def __init__(self, nome_mapa, foto_mapa):
        """
        Inicializa um novo mapa.

        Args:
            nome_mapa (str): Nome do mapa.
            foto_mapa (str): Caminho para a imagem do mapa.
        """
        self.nome_mapa = nome_mapa
        self.foto_mapa = foto_mapa
        self.icone_mapa = self.redimensionar_mapa()

    def __str__(self):
        """
        Returns:
            str: Nome do mapa.
        """
        return self.nome_mapa

    def __repr__(self):
        """
        Returns:
            str: Nome do mapa.
        """
        return self.nome_mapa

    def redimensionar_mapa(self):
        """
        Redimensiona a foto do mapa para se encaixar no card de arena
        """
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        relative_path = os.path.join(root, self.foto_mapa)
        imagem = Image.open(relative_path)
        imagem_redimensionada = imagem.resize((230, 120))
        return imagem_redimensionada


    def __eq__(self, other):
        """
        Compara dois mapas com base no nome.

        Args:
            other (Mapa): Outro objeto, idealmente Mapa.

        Returns:
            bool: True se os nomes forem iguais.
        """
        return isinstance(other, Mapa) and self.nome_mapa == other.nome_mapa

    def __hash__(self):
        """
        Permite que o objeto seja usado como chave em dicionários e sets.

        Returns:
            int: Hash baseado no nome do mapa.
        """
        return hash(self.nome_mapa)


class Vilarejo(Mapa):
    """
    Subclasse de Mapa que representa o cenário medieval "Vilarejo".

    Características:
        - Nome: "Vilarejo"
        - Caminho da imagem: 'assets/images/mapas/vilarejo.png'
    """
    def __init__(self):
        super().__init__('Vilarejo', 'assets/images/mapas/vilarejo.png')


class Torre(Mapa):
    """
    Subclasse de Mapa que representa o cenário externo "Torre".

    Características:
        - Nome: "Torre"
        - Caminho da imagem: 'assets/images/mapas/torre.png'
    """
    def __init__(self):
        super().__init__('Torre', 'assets/images/mapas/torre.png')
