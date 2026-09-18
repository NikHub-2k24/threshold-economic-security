import itertools
from typing import List, Tuple, Dict, Any
from .strategies import Strategy
from .game import Game
from models.payment_model import attacker_optimal_b_star, equal_split_b_star

def get_all_profiles(n: int) -> List[Tuple[Strategy, ...]]:
    return list(itertools.product(Strategy, repeat=n))

def is_pure_strategy_nash_equilibrium(game: Game, profile: Tuple[Strategy, ...]) -> bool:
    n = len(game.participants)
    for i in range(n):
        u_current = game.get_utility(i, profile)
        for s_i in Strategy:
            if s_i == profile[i]:
                continue
            dev_profile = list(profile)
            dev_profile[i] = s_i
            u_dev = game.get_utility(i, tuple(dev_profile))
            if u_dev > u_current:
                return False
    return True

def get_coalitions(n: int) -> List[List[int]]:
    coalitions = []
    for r in range(1, n + 1):
        coalitions.extend([list(c) for c in itertools.combinations(range(n), r)])
    return coalitions

def is_strict_coalition_stable(game: Game, profile: Tuple[Strategy, ...]) -> bool:
    n = len(game.participants)
    coalitions = get_coalitions(n)
    
    for C in coalitions:
        joint_strategies = list(itertools.product(Strategy, repeat=len(C)))
        for joint_strategy in joint_strategies:
            is_different = any(joint_strategy[idx] != profile[c_idx] for idx, c_idx in enumerate(C))
            if not is_different:
                continue
                
            dev_profile = list(profile)
            for idx, c_idx in enumerate(C):
                dev_profile[c_idx] = joint_strategy[idx]
            dev_profile = tuple(dev_profile)
            
            strictly_gains = True
            for c_idx in C:
                if game.get_utility(c_idx, dev_profile) <= game.get_utility(c_idx, profile):
                    strictly_gains = False
                    break
                    
            if strictly_gains:
                return False
    return True

def get_destabilization_thresholds(game: Game, baseline_profile: Tuple[Strategy, ...], split_rule: str = "attacker_optimal") -> Dict[str, Any]:
    n = len(game.participants)
    coalitions = get_coalitions(n)
    
    b_behavioral_star = float('inf')
    b_service_star = float('inf')
    
    behavioral_details = {}
    service_details = {}
    
    intrinsically_stable = is_strict_coalition_stable(game, baseline_profile)
    baseline_p_success = game.get_p_success(baseline_profile)
    
    for C in coalitions:
        joint_strategies = list(itertools.product(Strategy, repeat=len(C)))
        for joint_strategy in joint_strategies:
            is_different = any(joint_strategy[idx] != baseline_profile[c_idx] for idx, c_idx in enumerate(C))
            if not is_different:
                continue
                
            dev_profile = list(baseline_profile)
            for idx, c_idx in enumerate(C):
                dev_profile[c_idx] = joint_strategy[idx]
            dev_profile = tuple(dev_profile)
            
            dev_p_success = game.get_p_success(dev_profile)
            service_fails = (dev_p_success < baseline_p_success)
            
            r_values = []
            for c_idx in C:
                u_base = game.get_utility(c_idx, baseline_profile)
                u_dev = game.get_utility(c_idx, dev_profile)
                r_i = max(0.0, u_base - u_dev)
                r_values.append(r_i)
                
            if split_rule == "attacker_optimal":
                b_star_this_dev = attacker_optimal_b_star(r_values)
            elif split_rule == "equal_split":
                b_star_this_dev = equal_split_b_star(r_values)
            else:
                raise ValueError("Unknown split rule")
                
            details = {
                "coalition": C,
                "joint_deviation": tuple(joint_strategy),
                "reservation_prices": r_values,
                "dev_p_success": dev_p_success
            }
            
            if b_star_this_dev < b_behavioral_star:
                b_behavioral_star = b_star_this_dev
                behavioral_details = details
                
            if service_fails and b_star_this_dev < b_service_star:
                b_service_star = b_star_this_dev
                service_details = details
                
    return {
        "intrinsically_stable": intrinsically_stable,
        "baseline_p_success": baseline_p_success,
        "b_behavioral_star": b_behavioral_star if b_behavioral_star != float('inf') else None,
        "behavioral_details": behavioral_details if b_behavioral_star != float('inf') else None,
        "b_service_star": b_service_star if b_service_star != float('inf') else None,
        "service_details": service_details if b_service_star != float('inf') else None,
    }
