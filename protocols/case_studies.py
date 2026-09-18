# Abstract, simplified models inspired by research problems.
# Not connected to any external chain data.

def get_utxo_threshold_payment_config(n=5, t=3):
    return {
        "n": n, "t": t, "reward": 1.0, "cost": 0.1, "collateral": 10.0,
        "reliability": 0.99, "detection_probability_defect": 1.0
    }

def get_atomic_exchange_collusion_config(n=3, t=2):
    return {
        "n": n, "t": t, "reward": 5.0, "cost": 1.0, "collateral": 20.0,
        "reliability": 1.0, "detection_probability_defect": 0.5
    }

def get_threshold_oracle_config(n=8, t=5):
    return {
        "n": n, "t": t, "reward": 0.5, "cost": 0.2, "collateral": 2.0,
        "reliability": 0.95, "detection_probability_defect": 0.8
    }

def get_distributed_randomness_config(n=7, t=4):
    return {
        "n": n, "t": t, "reward": 2.0, "cost": 0.5, "collateral": 5.0,
        "reliability": 0.9, "detection_probability_defect": 1.0
    }
