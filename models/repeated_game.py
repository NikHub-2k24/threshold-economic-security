from typing import Tuple, List, Optional
from core.strategies import Strategy
from core.game import Game
from core.equilibrium import is_pure_strategy_nash_equilibrium, get_all_profiles

def find_pure_strategy_nash_equilibria(game: Game) -> List[Tuple[Strategy, ...]]:
    """
    Returns the complete set of pure-strategy Nash equilibria for the game.
    """
    n = len(game.participants)
    profiles = get_all_profiles(n)
    return [p for p in profiles if is_pure_strategy_nash_equilibrium(game, p)]

def check_grim_trigger_sustainability(
    game: Game, 
    baseline_profile: Tuple[Strategy, ...], 
    delta: float,
    punishment_profile: Optional[Tuple[Strategy, ...]] = None
) -> dict:
    
    if punishment_profile is None:
        equilibria = find_pure_strategy_nash_equilibria(game)
        if not equilibria:
            return {"computable": False, "reason": "No pure-strategy Nash equilibrium exists for punishment stage"}
        # Select the punishment profile that yields the minimum average utility (harshest punishment)
        # to maximize the threat of grim trigger.
        def avg_utility(p):
            return sum(game.get_utility(i, p) for i in range(len(game.participants))) / len(game.participants)
        punishment_profile = min(equilibria, key=avg_utility)
        
    elif not is_pure_strategy_nash_equilibrium(game, punishment_profile):
        return {"computable": False, "reason": "Provided punishment profile is not a pure-strategy Nash equilibrium"}
        
    n = len(game.participants)
    sustainable = True
    violators = []
    
    for i in range(n):
        u_h = game.get_utility(i, baseline_profile)
        u_p = game.get_utility(i, punishment_profile)
        
        max_u_dev = u_h
        for s_i in Strategy:
            if s_i == baseline_profile[i]:
                continue
            dev_profile = list(baseline_profile)
            dev_profile[i] = s_i
            u_dev = game.get_utility(i, tuple(dev_profile))
            if u_dev > max_u_dev:
                max_u_dev = u_dev
                
        gain = max_u_dev - u_h
        loss = (delta / (1.0 - delta)) * (u_h - u_p)
        
        if gain > loss:
            sustainable = False
            violators.append({
                "participant_id": i,
                "gain": gain,
                "loss": loss
            })
            
    return {
        "computable": True,
        "sustainable": sustainable,
        "punishment_profile": punishment_profile,
        "violators": violators
    }
