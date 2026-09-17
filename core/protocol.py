from dataclasses import dataclass

@dataclass(frozen=True)
class Protocol:
    n: int
    t: int
    detection_probability_defect: float = 1.0
    detection_probability_abstain: float = 0.0
