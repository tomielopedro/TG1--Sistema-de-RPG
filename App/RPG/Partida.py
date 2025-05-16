from dataclasses import dataclass, field
from typing import List
from .LogCombate import LogCombate

@dataclass
class Partida:
    id: int
    descricao: str
    logs: List[LogCombate] = field(default_factory=list)

    def adicionar_log(self, log: LogCombate):
        self.logs.append(log)

    def __str__(self):
        return f"Partida {self.id}: {self.descricao} com {len(self.logs)} ações"
