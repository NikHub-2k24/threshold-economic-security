from typing import Dict, Any, List
from core.strategies import Strategy
from core.participants import Participant
from core.protocol import Protocol
from core.adversary import AdversaryConfig
from core.game import Game
from core.equilibrium import get_destabilization_thresholds, is_pure_strategy_nash_equilibrium
from models.repeated_game import check_grim_trigger_sustainability

def run_experiment(config: Dict[str, Any]) -> Dict[str, Any]:
    n = config["n"]
    t = config["t"]
    reward = config["reward"]
    cost = config["cost"]
    collateral = config["collateral"]
    reliability = config["reliability"]
    risk_aversion = config.get("risk_aversion", 0.0)
    detection_probability_defect = config.get("detection_probability_defect", 1.0)
    detection_probability_abstain = config.get("detection_probability_abstain", 0.0)
    split_rule = config.get("split_rule", "attacker_optimal")
    delta = config.get("delta", 0.9)
    
    protocol = Protocol(
        n=n, 
        t=t, 
        detection_probability_defect=detection_probability_defect,
        detection_probability_abstain=detection_probability_abstain
    )
    
    participants = [
        Participant(
            id=i, 
            cost=cost, 
            reward=reward, 
            collateral=collateral, 
            reliability=reliability, 
            risk_aversion=risk_aversion
        ) for i in range(n)
    ]
    
    game = Game(protocol, participants, AdversaryConfig())
    baseline_profile = tuple([Strategy.HONEST] * n)
    
    result = {
        "n": n,
        "t": t,
        "reward": reward,
        "cost": cost,
        "collateral": collateral,
        "reliability": reliability,
        "split_rule": split_rule,
        "risk_aversion": risk_aversion,
        "detection_probability_defect": detection_probability_defect,
        "p_success": game.get_p_success(baseline_profile),
        "expected_payoff": sum(game.get_profile_utilities(baseline_profile)) / n,
    }
    
    if n <= 8:
        result["result_type"] = "Enumerated"
        result["nash_equilibrium"] = is_pure_strategy_nash_equilibrium(game, baseline_profile)
        

        thresholds = get_destabilization_thresholds(game, baseline_profile, split_rule)
        result["coalition_stable"] = thresholds["intrinsically_stable"]
        result["b_behavioral_star"] = thresholds["b_behavioral_star"]
        result["behavioral_details"] = thresholds.get("behavioral_details")
        result["b_service_star"] = thresholds["b_service_star"]
        result["service_details"] = thresholds.get("service_details")

        
        repeated = check_grim_trigger_sustainability(game, baseline_profile, delta)
        result["repeated_computable"] = repeated["computable"]
        if repeated["computable"]:
            result["repeated_sustainable"] = repeated["sustainable"]
            result["punishment_profile"] = str(repeated["punishment_profile"])
        else:
            result["repeated_sustainable"] = "NOT COMPUTED"
            result["punishment_profile"] = "NONE"
    else:
        result["result_type"] = "Simulated"
        result["nash_equilibrium"] = "NOT COMPUTED"
        result["coalition_stable"] = "NOT COMPUTED"
        result["b_behavioral_star"] = "NOT COMPUTED"
        result["b_service_star"] = "NOT COMPUTED"
        result["repeated_computable"] = False
        result["repeated_sustainable"] = "NOT COMPUTED"
        
    return result
