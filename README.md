# Threshold Economic Security Lab

When is a cryptographically decentralized service actually economically decentralized?

**Threshold Economic Security Lab** is a research-oriented computational framework for studying the gap between **cryptographic security assumptions** and **economic incentives** in threshold-based distributed services.

A threshold protocol may require, for example, `t` out of `n` participants to cooperate before a service can act. Cryptographically, the system may be secure as long as fewer than `t` participants are corrupted. Economically, however, an attacker may be able to **bribe, coordinate with, or otherwise incentivize rational participants** to deviate from the intended protocol.

This project models that problem explicitly.

It provides a mathematical game model, exact equilibrium analysis for small systems, probabilistic reliability calculations, bribery-threshold analysis, repeated-game analysis, parameter sweeps, and an interactive Streamlit interface for exploring the resulting security boundaries.

> **Research status:** this repository is a **research prototype/framework**, not a production cryptographic implementation and not, by itself, a claim of a new theorem or peer-reviewed research result. Its purpose is to make economic-security questions in threshold systems experimentally testable and reproducible.

## 1. Research Question

The central question is:

> **For a threshold service with `n` participants and threshold `t`, under what economic and adversarial conditions does honest participation cease to be incentive-compatible, and when does that loss of incentive compatibility become an actual service failure?**

This separates two questions that are often conflated:

1. **Individual incentive failure**: when does a participant have an economic reason to stop following the honest strategy?
2. **System failure**: when do enough participants deviate that the threshold service can no longer operate safely or reliably?

The project therefore studies the relationship:

```text
Protocol parameters
 │
 ├── n participants
 ├── threshold t
 ├── reward
 ├── execution cost
 ├── collateral
 ├── detection probability
 ├── availability
 ├── risk preference
 └── external incentive / bribe
 │
 ▼
Participant utilities
 │
 ▼
Strategic behaviour
 │
 ├── Honest
 ├── Abstain
 └── Defect
 │
 ▼
Equilibria + coalition stability
 │
 ▼
Economic security boundary
 │
 ├── Behavioral destabilization
 └── Service-failure destabilization
```

## 2. Why This Problem Matters

Threshold cryptography distributes trust among multiple parties rather than placing control in a single key holder. The same design pattern appears in systems such as:

* threshold signatures and multisignature custody,
* distributed oracles,
* distributed randomness systems,
* cross-chain and bridge infrastructure,
* threshold decryption,
* other committee-based cryptographic services.

Traditional cryptographic analysis often focuses on questions such as:

> How many participants must an attacker compromise?

An economic-security analysis asks an additional question:

> **How expensive is it to make otherwise rational participants participate in an attack?**

Those are not necessarily the same question. 

A system can remain cryptographically intact while becoming economically fragile if an external attacker can offer participants enough compensation to make deviation preferable to honest participation.

This project therefore treats **participant incentives as part of the security model**, rather than as an implementation detail.

## 3. What the Lab Actually Models

### 3.1 Threshold system

The basic service is parameterized by:

* `n`: number of participants
* `t`: number of successful contributions required for service success

A service succeeds when at least `t` required contributions are available.

For example:
```text
5-of-8 threshold service

Participants:
P1 P2 P3 P4 P5 P6 P7 P8

Required:
Any 5 valid contributions
```

The model can then ask what happens when some participants are unavailable, abstain, defect, or are economically incentivized to deviate.

## 4. Participant Strategies

Each participant chooses one of three base strategies:

**`honest`**
The participant contributes to the service when available.
They:
* pay the execution cost,
* receive the protocol reward when the service succeeds,
* remain exposed to the normal protocol incentives.

**`abstain`**
The participant does not contribute.
They receive no normal service reward and incur no execution cost.
The model can optionally include slashable abstention.

**`defect`**
The participant actively deviates from the prescribed protocol.
Depending on the model parameters, deviation can carry a probability of detection and a corresponding collateral loss.

Conceptually:
```text
        Participant
             │
 ┌───────────┼───────────┐
 │           │           │
 honest    abstain     defect
 │           │           │
reward-cost  0     attack payoff
                         │
                detection/collateral
```

## 5. Economic Utility Model

The project models each participant using a risk-adjusted expected utility.

The monetary component is:

```math
M_i(s) = P(\text{success} \mid s) \cdot \text{reward}_i(s_i) - \text{cost}_i(s_i) - P(\text{detected} \mid s) \cdot \text{collateral}_i(s_i) + B_{\text{external}, i}
```

where:
* `P(success | s)` is the probability that the threshold service succeeds under strategy profile `s`,
* `reward_i` is the participant's protocol reward,
* `cost_i` is the execution cost,
* `P(detected | s)` is the probability of detecting a deviation,
* `collateral_i` is the amount lost if the participant is detected,
* `B_external,i` is an external payment such as an attacker-funded bribe.

The risk-adjusted utility is:

```math
U_i(s) = M_i(s) - \rho_i \cdot Var_i(\text{payoff})
```

where `rho_i` captures the participant's sensitivity to payoff variance.

This allows the framework to distinguish between participants who have the same expected monetary payoff but different tolerance for risk.

In the baseline unbribed game:
```math
B_{\text{external}, i} = 0
```

## 6. External Incentives and Bribery

One of the main purposes of the framework is to vary external incentives and identify when they change strategic behaviour.

The project supports two bribery allocation models:

**Attacker-optimal bribery**
The attacker allocates the external reward in a way that minimizes the total cost of inducing the desired deviation.
This represents an attacker who is free to target participants differently.

**Equal-split bribery**
The external reward is distributed evenly among the targeted participants.
This represents a simpler coordination model and provides a useful comparison point.

The exact amount of an external incentive needed to change system behaviour becomes an experimentally measurable quantity.

## 7. Two Destabilization Thresholds

A central distinction in the project is between **behavioural destabilization** and **service-failure destabilization**.

### 7.1 Behavioral destabilization threshold

Define:
```math
B^*_{\text{behavioral}}
```
as the minimum external incentive at which an honest participant no longer prefers the honest action under the chosen model.

Conceptually:
```text
Bribe = 0
 │
 ▼
U(honest) > U(defect)
 │
 │ increase external incentive
 ▼
U(honest) = U(defect)
 │
 ▼
B*behavioral
 │
 ▼
Honesty is no longer strictly preferred
```
This is a statement about **individual incentive compatibility**.

### 7.2 Service-failure threshold

Define:
```math
B^*_{\text{service}}
```
as the minimum external incentive at which enough participants can be induced to deviate for the service to cross its operational threshold.

These quantities can differ substantially.

For example:
```text
One participant becomes willing to defect
 │
 ▼
 Behavioral boundary
 │
 │
 ▼
Several participants defect
 │
 ▼
Threshold t is no longer satisfied
 │
 ▼
 Service failure
```

This distinction is important because **an incentive-compatible system and a functioning system are not identical concepts**.

## 8. Probabilistic Reliability

The project does not treat participant availability as a simple deterministic variable.

Each participant can have an individual availability probability.

For example:
```text
P1: 0.98
P2: 0.94
P3: 0.91
P4: 0.87
P5: 0.95
...
```

The framework computes the probability that at least `t` participants are available using the **Poisson-binomial distribution**.

This is useful when participants have different reliability characteristics.
For a small system, the probability can be computed exactly rather than estimated through Monte Carlo sampling.

The result can answer questions such as:
> What is the probability that a `t-of-n` service fails purely because of availability?

That provides a baseline against which economically induced failures can be compared.

## 9. Equilibrium Analysis

For small systems, the framework performs **exact enumerative analysis**.

With `n <= 8`, it can exhaustively examine pure-strategy profiles and evaluate deviations.

The analysis includes:
* pure-strategy Nash equilibrium checks,
* strict coalition stability checks,
* joint deviations,
* utility comparisons across strategy profiles.

The objective is not merely to find the highest-payoff configuration. Instead, the system asks:

> **Given the incentives of every participant, which strategy profiles are stable against unilateral or specified joint deviations?**

For small systems this can be done exhaustively, which makes the results reproducible and avoids relying exclusively on stochastic search.

## 10. Coalition Stability

Individual rationality is not always sufficient.

A group of participants may have an incentive to coordinate even when no single participant would deviate alone.

The framework therefore distinguishes between:

```text
Unilateral deviation
 │
 ▼
"What happens if I deviate alone?"

Coalitional deviation
 │
 ▼
"What happens if several participants coordinate?"
```

This is particularly relevant to threshold systems because an attacker usually needs a **coalition large enough to change the threshold outcome**.

## 11. Repeated Games

The project also studies repeated interaction.

In a one-shot setting:
> What is my best action right now?

In a repeated setting:
> What is my best action when today's behaviour can affect future payoffs?

The framework includes a Grim-Trigger style repeated-game model in which cooperation can be sustained by future punishment following a deviation.

The analysis therefore examines whether the honest profile remains sustainable when participants repeatedly interact rather than treating each round as completely independent.

This matters because many real distributed systems are not one-shot games: the same operators may participate in the same protocol over long periods.

## 12. Experimental Outputs

The framework is designed to produce quantities that can be compared across parameter settings.

Typical outputs include:

**Incentive thresholds**
```text
B*behavioral
B*service
```

**Service reliability**
```text
P(service succeeds)
P(service fails)
```

**Equilibrium structure**
```text
Pure-strategy Nash equilibria
Stable / unstable profiles
Coalitionally stable profiles
```

**Parameter sensitivity**
Examples:
```text
threshold t
number of participants n
reward
execution cost
collateral
detection probability
availability
risk aversion
external incentive
```

**Visualizations**
The Streamlit interface can be used to inspect:
* incentive curves,
* threshold matrices,
* parameter sweeps,
* equilibrium outcomes,
* service-failure boundaries.

## 13. Research Workflow

A typical experiment can follow this sequence:

```text
1. Define a threshold system
 │
 ▼
2. Specify participant incentives
 │
 ▼
3. Specify availability and detection assumptions
 │
 ▼
4. Enumerate equilibria / run simulations
 │
 ▼
5. Introduce external incentives
 │
 ▼
6. Locate behavioral destabilization
 │
 ▼
7. Locate service-failure destabilization
 │
 ▼
8. Sweep parameters
 │
 ▼
9. Compare security boundaries
 │
 ▼
10. Export reproducible results
```

This makes the repository useful as a computational laboratory rather than as a single hard-coded experiment.

## 14. Project Structure

```text
threshold-economic-security/
│
├── app/
│   └── Streamlit application
│
├── cli/
│   └── Command-line experiment runners and report generation
│
├── core/
│   └── Mathematical engine
│       ├── strategies
│       ├── utilities
│       ├── incentives
│       └── equilibrium analysis
│
├── experiments/
│   └── Parameter sweeps and experiment orchestration
│
├── models/
│   └── Game-theoretic extensions
│       ├── bribery / payment rules
│       └── repeated-game sustainability
│
├── protocols/
│   └── Abstract protocol examples and educational scaffolding
│
├── tests/
│   └── Mathematical and behavioural validation tests
│
├── requirements.txt
├── test_config.json
└── README.md
```

The separation is intentional:
* `core/` contains the mathematical logic.
* `models/` extends that logic with game-theoretic mechanisms.
* `experiments/` connects the model to parameter sweeps.
* `app/` provides interactive exploration.
* `cli/` supports reproducible, headless experiments.
* `protocols/` provides examples without pretending to be production cryptography.
* `tests/` checks the mathematical engine against known edge cases.

## 15. Installation

**Requirements**
* Python 3.9+
* `pip`
* Recommended: a virtual environment

**Clone**
```bash
git clone https://github.com/NikHub-2k24/threshold-economic-security.git
cd threshold-economic-security
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

## 16. Run the Interactive Lab

**Windows PowerShell**
```bash
$env:PYTHONPATH="."
streamlit run app/main.py
```

**Linux / macOS**
```bash
PYTHONPATH="." streamlit run app/main.py
```

The Streamlit application provides a GUI for constructing experiments, running analyses, exploring parameter changes, and visualizing results.

## 17. Run CLI Experiments

The project also supports non-interactive experiments.

**Windows PowerShell**
```bash
$env:PYTHONPATH="."
python cli/run_experiment.py --config test_config.json --outdir results/
```

**Linux / macOS**
```bash
PYTHONPATH="." python cli/run_experiment.py \
    --config test_config.json \
    --outdir results/
```

The experiment runner can be used for larger parameter sweeps and automated report generation.

Typical outputs include:
```text
results/
├── JSON data
├── CSV tables
└── Markdown research reports
```

## 18. Testing

The mathematical core is tested against hand-computed edge cases and expected behavioural properties.

Run:

**Windows**
```bash
$env:PYTHONPATH="."
pytest
```

**Linux / macOS**
```bash
PYTHONPATH="." pytest
```

The goal of these tests is not merely to test whether the UI runs. The important target is the correctness of the underlying mathematical engine.

## 19. Scope and Limitations

This project is deliberately an **abstract economic-security model**.

It should not be interpreted as a complete model of any specific production protocol.

**The project does not:**
* execute live cryptographic protocols,
* manage real private keys,
* connect to blockchain networks,
* parse live smart-contract state,
* consume real-time token prices,
* model every possible adversarial strategy,
* guarantee that a model's equilibrium prediction matches real participant behaviour,
* replace a protocol-specific security proof,
* provide production-ready cryptographic primitives.

The included toy cryptographic examples are educational scaffolding only.

**Important modelling assumptions**
The current framework simplifies real systems in several ways:
* participant behaviour is represented using a limited strategy set,
* utilities are specified parametrically,
* the external incentive model is simplified,
* participant information is not necessarily private,
* real-world coordination costs are abstracted,
* legal, reputational and institutional effects are not fully modelled,
* exact equilibrium enumeration becomes computationally expensive as `n` grows.

These limitations are not hidden assumptions. They define the boundary within which the experimental results should be interpreted.

## 20. What Counts as a Research Result Here?

Running the software and producing a graph is not automatically a scientific contribution.

The framework is designed to support questions such as:
* How does the minimum attack incentive change as `t/n` changes?
* When does increasing collateral meaningfully increase economic security?
* How does imperfect detection change the attack threshold?
* Under heterogeneous participant risk preferences, does the weakest participant determine the system's economic security?
* How different are behavioural and service-failure thresholds?
* When does repeated interaction sustain honest behaviour that is not sustainable in a one-shot game?
* How sensitive are the conclusions to the bribery allocation mechanism?
* How does participant heterogeneity change coalition formation?
* Which combinations of rewards, penalties, thresholds and availability produce robust incentive compatibility?

A strong research result should go beyond:
> "The program produced this graph."

It should identify a **generalizable relationship, bound, phenomenon, counterexample, or mechanism-design insight** and justify it mathematically or experimentally.

## 21. Positioning Relative to Existing Research

The repository builds on an established research area at the intersection of:
* threshold cryptography,
* game theory,
* mechanism design,
* distributed systems,
* cryptoeconomics,
* security economics.

Relevant prior work includes:

**Yakira, Grayevsky & Asayag (2019), Rational Threshold Cryptosystems.**
Studies threshold cryptosystems when participants are rational, profit-maximizing entities and identifies collusion as a central threat.

**Tas & Boneh (2023), Cryptoeconomic Security for Data Availability Committees.**
Studies rational committee participants, adversarial corruption and bribery in data-availability systems and analyzes economic incentives for secure behaviour.

**Zhang et al. (2023), Breaking Blockchain Rationality with Out-of-Band Collusion.**
Studies how external incentives can make protocol deviation rational even when the original protocol assumes participants maximize their internal protocol rewards.

The purpose of this repository is not to claim that these problems are new. It is to provide a reusable computational framework in which related economic-security questions can be formulated, compared, and experimentally investigated.

## 22. Research Directions

Possible extensions include:

**Mechanism design**
Instead of only measuring when a system becomes economically unstable, search for protocol parameters that maximize resistance to bribery.

```text
Choose:
    rewards
    collateral
    threshold
    detection probability
    penalties

Subject to:
    acceptable service reliability
    acceptable operating cost

Optimize:
    minimum attack incentive
```

**Heterogeneous participants**
Allow participants to differ in:
* cost,
* collateral,
* risk aversion,
* availability,
* rewards,
* opportunity cost.
This creates more realistic economic asymmetry.

**Coalition formation**
Move beyond fixed deviation sets and model how rational attackers construct profitable coalitions.

**Dynamic attackers**
Allow the attacker's budget or expected profit to depend on the state of the underlying service.

**Protocol-specific case studies**
Instantiate the framework with carefully documented abstractions of:
* threshold custody,
* bridges,
* oracle committees,
* distributed randomness,
* data-availability committees.

**Theoretical results**
Use the computational model to discover candidate patterns and then attempt to prove general bounds or theorems.
That last step is especially important if the goal is a formal academic contribution.

## 23. A Useful Conceptual Distinction

The project's core idea can be summarized as:

```math
\text{Cryptographic security} \neq \text{Economic security}
```

A threshold may be mathematically difficult to violate while still being economically cheap to attack.

The framework therefore treats economic incentives as another layer of the security model:

```text
 Cryptographic assumptions
           │
           ▼
  Threshold structure
           │
           ▼
 Participant incentives
           │
  ┌────────┴────────┐
  ▼                 ▼
Honest play    Deviations
  │                 │
  └────────┬────────┘
           ▼
      Equilibrium
           │
           ▼
   Economic security
           │
           ▼
     System outcome
```

## 24. License

This project is released under the MIT License. See `LICENSE` for details.
