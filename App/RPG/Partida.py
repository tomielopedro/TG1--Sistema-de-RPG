from dataclasses import dataclass, field
from typing import List, Optional
from .LogCombate import LogCombate
import uuid

@dataclass
class Partida:
    """
    Classe que representa uma partida (batalha) realizada entre personagens em uma arena.

    Atributos:
        id (str): Identificador único da partida. Pode ser gerado com `uuid.uuid4().hex`.
        descricao (str): Descrição textual da partida (ex: "Batalha Total", "Duelo 1x1").
        logs (List[LogCombate]): Lista de eventos de combate (ataques, habilidades, etc.) ocorridos durante a partida.
        vencedor (Optional[str]): Nome do personagem vencedor da partida (caso definido).

    Métodos:
        adicionar_log(log: LogCombate): Adiciona um novo registro de evento à lista de logs da partida.
    """

    id: str
    descricao: str
    logs: List[LogCombate] = field(default_factory=list)
    vencedor: Optional[str] = None

    def adicionar_log(self, log: LogCombate):
        """
        Adiciona um log de combate à lista de eventos da partida.

        Args:
            log (LogCombate): Instância contendo os detalhes do evento de combate a ser registrado.
        """
        self.logs.append(log)
