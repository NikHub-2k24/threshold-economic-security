import os

readme = r"""# Threshold Fairness Lab

*When is a cryptographically decentralized service actually economically decentralized?*

**Threshold Fairness Lab** is a local, offline research tool designed to analyze the economic incentive-compatibility of threshold cryptographic services (e.g., $t$-of-$n$ multisig, threshold oracles, distributed randomness, atomic swaps). 

While cryptographic protocols define what participants *can* do, this tool evaluates what rational or adversarial participants *will* do when faced with external incentives, bribery, collusion, and the realities of distributed system failures.

---

## ?? Core Research Question

> *For a threshold service with $n$ participants and threshold $t$, under what economic and adversarial conditions does the honest strategy cease to be incentive-compatible?*

This platform allows researchers to construct a threshold protocol model, define participant incentives, run enumerative exact-equilibrium experiments (or large-scale simulations), and visualize outcomes like the **Service-Failure Frontier** and **Incentive Thresholds ($B^*$ )**.

## ? Features

- **Exact Enumerative Analysis ($n \le 8$)**: Exhaustively calculates pure-strategy Nash equilibria and strict coalition stability by evaluating every possible joint deviation.
- **Probabilistic Reliability Modeling**: Computes exact service-failure probabilities using the Poisson Binomial Probability Mass Function (no Monte Carlo required for small $n$).
- **External Incentive Analysis**: Calculates both Behavioral Destabilization ($B_{behavioral}^*$) and Service-Failure Destabilization ($B_{service}^*$) thresholds using Attacker-Optimal and Equal-Split bribery rules.
- **Repeated Game Modeling**: Evaluates the sustainability of the honest profile in an infinite-horizon setting using Grim-Trigger strategies against explicit pure-strategy Nash punishment profiles.
- **Interactive Streamlit UI**: A clean, research-focused dashboard to build experiments, run parameter sweeps, and visualize threshold matrices and incentive curves.
- **CLI & Automated Reporting**: Run offline parameter sweeps and export results to JSON, CSV, and formatted Markdown research reports.

## ?? The Mathematical Model

### Participant Actions
Participants choose a base strategy from exactly three options:
- **`honest`**: Contributes to the service when available. Pays an execution $cost$, and receives a $reward$ if the service succeeds.
- **`abstain`**: Contributes nothing. Pays 0, receives 0. (Optionally slashable).
- **`defect`**: Actively attacks or equivocates. Pays 0, receives 0. Detected with a specific probability, resulting in the loss of $collateral$.

### Utility Function
The risk-adjusted expected utility $U_i$ for a participant is calculated as:
$$M_i(s) = P(\text{success} \mid s) \cdot \text{reward}_i(s_i) - \text{cost}_i(s_i) - P(\text{detected} \mid s) \cdot \text{collateral}_i(s_i) + \text{external\_bribe}_i$$
$$U_i(s) = M_i(s) - \rho_i \cdot Var_i(\text{payoff})$$

*(Note: In the baseline unbribed game, $\text{external\_bribe}_i = 0$ for all participants).*

## ?? Getting Started

### Prerequisites
- Python 3.9+
- Recommended: A virtual environment (`venv` or `conda`)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/threshold-fairness-lab.git
cd threshold-fairness-lab
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Interactive Lab (Streamlit)
Launch the graphical interface to interactively build and visualize experiments:
```bash
# Windows
$env:PYTHONPATH="."
streamlit run app/main.py

# Linux / macOS
PYTHONPATH="." streamlit run app/main.py
```

### Running CLI Parameter Sweeps
For headless operation and large-scale data generation:
```bash
# 1. Create a configuration file (e.g., config.json)
# 2. Run the experiment runner
# Windows:
$env:PYTHONPATH="." 
python cli/run_experiment.py --config test_config.json --outdir results/

# Linux / macOS:
PYTHONPATH="." python cli/run_experiment.py --config test_config.json --outdir results/
```

## ?? Project Structure

- `/core`: The strict mathematical engine (strategies, incentives, utility calculation, equilibrium enumeration).
- `/models`: Game theory extensions (payment splitting rules, repeated game sustainability).
- `/experiments`: Logic bridging the mathematical core and parameter sweeping.
- `/app`: The Streamlit web application (Landing page, Experiment Builder, Results, Graphs, Methodology).
- `/cli`: Command-line wrappers and automated Markdown research report generators.
- `/protocols`: Abstract case studies and educational scaffolding (e.g., toy Shamir Secret Sharing).
- `/tests`: Pytest suite containing rigorously hand-computed baseline mathematical assertions.

## ?? Testing

The mathematical core is strictly verified against hand-computed exact edge-cases. To run the test suite:
```bash
# Windows
$env:PYTHONPATH="."
pytest

# Linux / macOS
PYTHONPATH="." pytest
```

## ?? Scope Exclusions
This is an **abstract research model** of economic incentives.
- It does **NOT** execute cryptographic code on live networks.
- It does **NOT** parse blockchain state, smart contracts, or real-time token prices.
- The included `/protocols/toy_crypto.py` is explicitly for educational scaffolding and is **not secure for production**.

## ?? License
This project is licensed under the MIT License - see the LICENSE file for details.
"""

contributing_text = r"""# Contributing to Threshold Fairness Lab

Thank you for your interest in contributing to the Threshold Fairness Lab! We welcome contributions from researchers, economists, and developers.

## ?? Important Mathematical Rule

The core engine (`/core`) of this tool implements a strict, verified mathematical model regarding pure-strategy Nash equilibria, strict coalition stability, and probabilistic reliability. 

**Do NOT submit PRs that:**
- Introduce arbitrary heuristic "security scores"
- Break the independent Bernoulli probability assumptions without explicitly updating the mathematical specification
- Replace exact enumeration with Monte Carlo simulation for $n \le 8$

If you find a genuine mathematical bug in the core engine, please open an Issue with the formal mathematical derivation before submitting a PR.

## ??? How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write your feature
4. **Write tests** in `/tests` for any core engine changes
5. Run the existing tests (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
with open("CONTRIBUTING.md", "w", encoding="utf-8") as f:
    f.write(contributing_text)
