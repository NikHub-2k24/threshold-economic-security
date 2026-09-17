from typing import Tuple, List, Dict
import math

from .strategies import Strategy
from .participants import Participant
from .protocol import Protocol

def poisson_binomial_pmf(probabilities: List[float]) -> List[float]:
    n = len(probabilities)
    pmf = [1.0]
    for p in probabilities:
        next_pmf = [0.0] * (len(pmf) + 1)
        for k in range(len(pmf)):
            next_pmf[k + 1] += pmf[k] * p
            next_pmf[k] += pmf[k] * (1.0 - p)
        pmf = next_pmf
    return pmf

def probability_service_succeeds(
    protocol: Protocol, 
    participants: List[Participant], 
    profile: Tuple[Strategy, ...]
) -> float:
    honest_reliabilities = [
        p.reliability for p, s in zip(participants, profile) if s == Strategy.HONEST
    ]
    if not honest_reliabilities:
        return 1.0 if protocol.t <= 0 else 0.0
    pmf = poisson_binomial_pmf(honest_reliabilities)
    t = protocol.t
    if t > len(pmf) - 1:
        return 0.0
    if t <= 0:
        return 1.0
    return sum(pmf[t:])

def expected_payoff(
    participant_idx: int,
    protocol: Protocol,
    participants: List[Participant],
    profile: Tuple[Strategy, ...],
    p_success: float
) -> Tuple[float, float]:
    participant = participants[participant_idx]
    s_i = profile[participant_idx]
    
    cost = 0.0
    reward = 0.0
    p_detected = 0.0
    slash = participant.collateral
    
    if s_i == Strategy.HONEST:
        cost = participant.cost
        reward = participant.reward
    elif s_i == Strategy.DEFECT:
        p_detected = protocol.detection_probability_defect
    elif s_i == Strategy.ABSTAIN:
        p_detected = protocol.detection_probability_abstain
            
    expected_m = (p_success * reward) - cost - (p_detected * slash)
    
    if s_i == Strategy.HONEST:
        var_m = (reward ** 2) * p_success * (1.0 - p_success)
    else:
        var_m = (slash ** 2) * p_detected * (1.0 - p_detected)
        
    return expected_m, var_m

def utility(
    participant_idx: int,
    protocol: Protocol,
    participants: List[Participant],
    profile: Tuple[Strategy, ...],
    p_success: float
) -> float:
    m_i, var_i = expected_payoff(participant_idx, protocol, participants, profile, p_success)
    participant = participants[participant_idx]
    return m_i - (participant.risk_aversion * var_i)
