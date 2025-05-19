from dataclasses import dataclass
from typing import Optional

@dataclass
class LogCombate:
    """
    Classe que representa o registro (log) detalhado de uma ação de combate entre dois personagens.
    Atributos:
        atacante (str):  Nome do personagem que realizou o ataque.
        atacante_classe (str):  Classe do personagem atacante (ex: Guerreiro, Mago).
        alvo (str):   Nome do personagem que foi alvo do ataque.
        alvo_classe (str):  Classe do personagem alvo.
        alvo_vida (int):  Pontos de vida do alvo após o ataque.
        alvo_pontos_defesa (int):  Pontos de defesa do alvo no momento do ataque.
        numero_d20 (Optional[int]):  Número sorteado no dado D20 para verificar chance de acerto (Pode ser None se não usado).
        chance_ataque (Optional[int]):  Valor total calculado da chance de acerto do ataque (ex: soma de ataque e dado).
        ataque_bem_sucedido (bool):  Indica se o ataque foi bem-sucedido.
        ataque_total (int):  Valor total de dano (ou cura) causado pelo ataque ou habilidade.
        habilidade_ataque (Optional[str]):   Nome da habilidade usada, se houver.
        descricao_habilidade (Optional[str]): Descrição textual da habilidade usada.
    """
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
