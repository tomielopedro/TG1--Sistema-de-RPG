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
    Representa uma arena de combate onde ocorrem várias partidas entre personagens.

    Atributos:
        nome_arena (str): Nome da arena.
        tipo_jogo (str): Tipo da arena (ex: PVP, Equipe).
        limite_jogadores (int): Máximo de jogadores permitidos.
        mapa (str): Nome do mapa da arena.
        lista_personagens (List[Personagem]): Personagens presentes na arena.
        partidas (List[Partida]): Histórico de partidas realizadas.
        partida_atual (Optional[Partida]): Partida em andamento.
    """

    def __init__(self, nome_arena, tipo_de_jogo, mapa):
        self.nome_arena = nome_arena
        self.tipo_jogo = tipo_de_jogo.nome
        self.limite_jogadores = tipo_de_jogo.limite_jogadores
        self.icone = tipo_de_jogo.icone
        self.mapa = mapa.nome_mapa
        self.foto_mapa = mapa.foto_mapa

        self.lista_personagens: List[Personagem] = []
        self.partidas: List[Partida] = []
        self.partida_atual: Optional[Partida] = None
        self.contador_partidas = 0

    def add_personagens(self, personagem: Personagem):
        """Adiciona um personagem válido à arena."""
        if isinstance(personagem, Personagem):
            self.lista_personagens.append(personagem.__copy__())

    def remove_personagem(self, personagem: Personagem):
        """Remove um personagem da arena, se estiver presente."""
        if isinstance(personagem, Personagem) and personagem in self.lista_personagens:
            self.lista_personagens.remove(personagem)

    def iniciar_nova_partida(self, descricao: str = ""):
        """Inicia uma nova partida, armazenando a anterior se houver."""
        self.contador_partidas += 1
        nova_partida = Partida(id=str(uuid.uuid4()), descricao=descricao)
        self.partida_atual = nova_partida
        self.partidas.append(nova_partida)


    def combate(self, atacante: Personagem, alvo: Personagem) -> LogCombate:
        """
        Executa um combate entre dois personagens e registra o log na partida atual.

        Retorna:
            LogCombate: Registro detalhado do combate.
        """
        log = LogCombate(
            atacante=atacante.nome,
            atacante_classe=getattr(atacante.classe, 'nome', 'Desconhecido'),
            alvo=alvo.nome,
            alvo_classe=getattr(alvo.classe, 'nome', 'Desconhecido'),
            alvo_vida=alvo.pontos_vida,
            alvo_pontos_defesa=alvo.pontos_defesa
        )

        if not isinstance(atacante, Personagem) or not isinstance(alvo, Personagem):
            if self.partida_atual:
                self.partida_atual.adicionar_log(log)
            return log

        if atacante not in self.lista_personagens or alvo not in self.lista_personagens:
            if self.partida_atual:
                self.partida_atual.adicionar_log(log)
            return log

        numero_d20 = D20().jogar()
        chance_ataque = atacante.pontos_ataque + numero_d20
        log.numero_d20 = numero_d20
        log.dano_ataque = chance_ataque
        log.ataque_bem_sucedido = chance_ataque > alvo.pontos_defesa

        if log.ataque_bem_sucedido:
            ataque_total, habilidade = atacante.atacar(alvo)
            log.ataque_total = ataque_total
            log.alvo_vida = alvo.pontos_vida
            if habilidade:
                log.habilidade_ataque = habilidade.nome
                log.descricao_habilidade = habilidade.descricao

        if self.partida_atual:
            self.partida_atual.adicionar_log(log)

        return log

    def __eq__(self, other):
        """Duas arenas são iguais se tiverem o mesmo nome."""
        return isinstance(other, Arena) and self.nome_arena == other.nome_arena

    def __str__(self):
        return f"Arena '{self.nome_arena}' ({self.tipo_jogo}) - Mapa: {self.mapa}"

    def __repr__(self):
        return self.nome_arena


