import re

with open("experiments/experiment_runner.py", "r") as f:
    content = f.read()

replacement = """
        thresholds = get_destabilization_thresholds(game, baseline_profile, split_rule)
        result["coalition_stable"] = thresholds["intrinsically_stable"]
        result["b_behavioral_star"] = thresholds["b_behavioral_star"]
        result["behavioral_details"] = thresholds.get("behavioral_details")
        result["b_service_star"] = thresholds["b_service_star"]
        result["service_details"] = thresholds.get("service_details")
"""

content = re.sub(r'        thresholds = get_destabilization_thresholds\(game, baseline_profile, split_rule\).*?result\["b_service_star"\] = thresholds\["b_service_star"\]', replacement, content, flags=re.DOTALL)

with open("experiments/experiment_runner.py", "w") as f:
    f.write(content)
