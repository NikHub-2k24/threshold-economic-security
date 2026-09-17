import time
from experiments.experiment_runner import run_experiment

start = time.time()
n = 8
t = 4
cfg = {
    "n": n, "t": t, "reward": 10.0, "cost": 2.0, "collateral": 5.0, 
    "reliability": 1.0, "risk_aversion": 0.0,
    "detection_probability_defect": 1.0, "detection_probability_abstain": 0.0,
    "split_rule": "attacker_optimal"
}
run_experiment(cfg)
print(f"Time for n=8: {time.time() - start:.2f}s")
