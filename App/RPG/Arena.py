from .Personagem import Personagem
from .Habilidade import *
from .Dados import *
from .Mapa import *
from .LogCombate import LogCombate
from .Partida import Partida
from typing import List, Optional
import uuid


class Arena:
    """
    Representa uma arena de combate onde ocorrem partidas entre personagens.

    Atributos:
        nome_arena (str): Nome identificador da arena.
        tipo_jogo (str): Tipo de jogo (ex: "X1", "PVP").
        limite_jogadores (int): Número máximo de jogadores permitidos na arena.
        icone (str): Caminho para o ícone visual do tipo de jogo.
        mapa (str): Nome do mapa utilizado na arena.
        foto_mapa (str): Caminho da imagem do mapa.
        lista_personagens (List[Personagem]): Lista de personagens participando da arena.
        partidas (List[Partida]): Histórico de partidas realizadas na arena.
        partida_atual (Optional[Partida]): Referência para a partida atualmente em andamento.
        contador_partidas (int): Contador de partidas realizadas.
    """

    def __init__(self, nome_arena, tipo_de_jogo, mapa):
        """
        Inicializa uma nova arena de combate.

        Args:
            nome_arena (str): Nome da arena.
            tipo_de_jogo (TipoJogo): Tipo de jogo (ex: X1, PVP).
            mapa (Mapa): Mapa no qual as batalhas ocorrem.
        """
        self.nome_arena = nome_arena
        self.tipo_jogo = tipo_de_jogo
        self.limite_jogadores = tipo_de_jogo.limite_jogadores
        self.icone = tipo_de_jogo.icone
        self.mapa = mapa
        self.foto_mapa = mapa.foto_mapa

        self.lista_personagens: List[Personagem] = []
        self.partidas: List[Partida] = []
        self.partida_atual: Optional[Partida] = None
        self.contador_partidas = 0

    def add_personagens(self, personagem: Personagem):
        """
        Adiciona uma cópia de um personagem à arena, evitando efeitos colaterais.

        Args:
            personagem (Personagem): Personagem a ser adicionado.
        """
        if isinstance(personagem, Personagem):
            self.lista_personagens.append(personagem.__copy__())

    def remove_personagem(self, personagem: Personagem):
        """
        Remove um personagem da arena, se ele estiver presente.

        Args:
            personagem (Personagem): Personagem a ser removido.
        """
        if isinstance(personagem, Personagem) and personagem in self.lista_personagens:
            self.lista_personagens.remove(personagem)

    def iniciar_nova_partida(self, descricao: str = ""):
        """
        Inicia uma nova partida, salvando a anterior (se existir).

        Args:
            descricao (str): Descrição opcional da partida (ex: "Batalha Final").
        """
        self.contador_partidas += 1
        nova_partida = Partida(id=str(uuid.uuid4()), descricao=descricao)
        self.partida_atual = nova_partida
        self.partidas.append(nova_partida)

    def combate(self, atacante: Personagem, alvo: Personagem) -> LogCombate:
        """
        Executa um turno de combate entre dois personagens, registrando o evento.

        Regras:
        - Usa um D20 para determinar chance de acerto.
        - Se a chance de ataque for maior que a defesa do alvo, o ataque acontece.
        - Se uma habilidade for usada (como cura), ela é registrada.
        - O log é salvo na partida atual.

        Args:
            atacante (Personagem): Personagem que realiza o ataque.
            alvo (Personagem): Personagem que é alvo do ataque.

        Returns:
            LogCombate: Objeto contendo o registro detalhado do combate.
        """
        log = LogCombate(
            atacante=atacante.nome,
            atacante_classe=getattr(atacante.classe, 'nome', 'Desconhecido'),
            alvo=alvo.nome,
            alvo_classe=getattr(alvo.classe, 'nome', 'Desconhecido'),
            alvo_vida=alvo.pontos_vida,
            alvo_pontos_defesa=alvo.pontos_defesa
        )

        # Validação: só executa combate se ambos forem Personagem e estiverem na lista
        if isinstance(atacante, Personagem) and isinstance(alvo, Personagem):
            if atacante in self.lista_personagens and alvo in self.lista_personagens:
                numero_d20 = D20().jogar()
                chance_ataque = atacante.pontos_ataque + numero_d20
                log.numero_d20 = numero_d20
                log.chance_ataque = chance_ataque
                log.ataque_bem_sucedido = chance_ataque > alvo.pontos_defesa

                if log.ataque_bem_sucedido:
                    ataque_total, habilidade = atacante.atacar(alvo)
                    log.ataque_total = ataque_total
                    log.alvo_vida = alvo.pontos_vida
                    if habilidade:
                        log.habilidade_ataque = habilidade.nome
                        log.descricao_habilidade = habilidade.descricao

        return log

    def __eq__(self, other):
        """
        Compara duas arenas com base no nome.

        Args:
            other (Arena): Outra instância de arena.

        Returns:
            bool: True se os nomes forem iguais, False caso contrário.
        """
        return isinstance(other, Arena) and self.nome_arena == other.nome_arena

    def __str__(self):
        """
        Retorna uma string representando a arena.

        Returns:
            str: Nome, tipo e mapa da arena.
        """
        return f"Arena '{self.nome_arena}' ({self.tipo_jogo}) - Mapa: {self.mapa}"

    def __repr__(self):
        """
        Representação informal da arena.

        Returns:
            str: Nome da arena.
        """
        return self.nome_arena
