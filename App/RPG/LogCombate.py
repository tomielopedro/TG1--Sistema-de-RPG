from dataclasses import dataclass
from typing import Optional



@dataclass
class LogCombate:
    atacante: str
    atacante_classe: str
    alvo: str
    alvo_classe: str
    alvo_vida: int
    alvo_pontos_defesa: int
    numero_d20: Optional[int] = None
    chance_ataque: Optional[int] = None
    ataque_bem_sucedido: bool = False
    ataque_total: int = 0
    habilidade_ataque: Optional[str] = None
    descricao_habilidade: Optional[str] = None
