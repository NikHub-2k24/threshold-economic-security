import sys
import json
import csv
import argparse
import os

# Add parent directory to path so it can be run standalone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from experiments.experiment_runner import run_experiment

def main():
    parser = argparse.ArgumentParser(description="Run Threshold Fairness Lab experiments.")
    parser.add_argument("--config", type=str, required=True, help="Path to JSON config file")
    parser.add_argument("--outdir", type=str, default="results", help="Output directory")
    args = parser.parse_args()
    
    with open(args.config, "r") as f:
        config_list = json.load(f)
        
    if not isinstance(config_list, list):
        config_list = [config_list]
        
    results = []
    for cfg in config_list:
        results.append(run_experiment(cfg))
        
    os.makedirs(args.outdir, exist_ok=True)
    
    with open(os.path.join(args.outdir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
        
    if results:
        keys = results[0].keys()
        with open(os.path.join(args.outdir, "results.csv"), "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
            
    print(f"Experiments completed. Results exported to {args.outdir}/")

if __name__ == "__main__":
    main()
