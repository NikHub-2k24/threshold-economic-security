import os
import json
import csv

def generate_research_report(outdir="results"):
    os.makedirs(outdir, exist_ok=True)
    report = """# Research Report

## Question
[insufficient data to conclude]

## Model
[insufficient data to conclude]

## Assumptions
[insufficient data to conclude]

## Threat Model
[insufficient data to conclude]

## Experimental Design
[insufficient data to conclude]

## Results
[insufficient data to conclude]

## Sensitivity Analysis
[insufficient data to conclude]

## Unexpected Findings
[insufficient data to conclude]

## Limitations
[insufficient data to conclude]

## Open Questions
[insufficient data to conclude]
"""
    with open(os.path.join(outdir, "README.md"), "w") as f:
        f.write(report)
        
    print("Research report generated.")

if __name__ == "__main__":
    generate_research_report()
