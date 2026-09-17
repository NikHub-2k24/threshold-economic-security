from dataclasses import dataclass

@dataclass(frozen=True)
class Participant:
    id: int
    cost: float
    reward: float
    collateral: float
    reliability: float
    risk_aversion: float = 0.0
