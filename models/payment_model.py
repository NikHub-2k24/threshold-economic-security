from typing import List

def attacker_optimal_b_star(r_values: List[float]) -> float:
    return sum(r_values)

def equal_split_b_star(r_values: List[float]) -> float:
    if not r_values:
        return 0.0
    return len(r_values) * max(r_values)
