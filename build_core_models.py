import os

with open('core/strategies.py', 'w') as f:
    f.write('''from enum import Enum

class Strategy(Enum):
    HONEST = "honest"
    ABSTAIN = "abstain"
    DEFECT = "defect"
''')

with open('core/participants.py', 'w') as f:
    f.write('''from dataclasses import dataclass

@dataclass(frozen=True)
class Participant:
    id: int
    cost: float
    reward: float
    collateral: float
    reliability: float
    risk_aversion: float = 0.0
''')

with open('core/protocol.py', 'w') as f:
    f.write('''from dataclasses import dataclass

@dataclass(frozen=True)
class Protocol:
    n: int
    t: int
    detection_probability: float = 1.0
    abstain_slashable: bool = False
''')

with open('core/thresholds.py', 'w') as f:
    f.write('''def threshold_service_succeeds(available_honest_count: int, t: int) -> bool:
    return available_honest_count >= t
''')

with open('core/adversary.py', 'w') as f:
    f.write('''from dataclasses import dataclass

@dataclass(frozen=True)
class AdversaryConfig:
    pass
''')
