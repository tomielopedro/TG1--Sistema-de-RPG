from dataclasses import dataclass, field
from typing import List
from .LogCombate import LogCombate
from typing import Optional
import uuid
@dataclass
class Partida:
    id: str
    descricao: str
    logs: List[LogCombate] = field(default_factory=list)
    vencedor: Optional[str] = None

    def adicionar_log(self, log: LogCombate):
        self.logs.append(log)