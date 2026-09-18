import streamlit as st

st.set_page_config(page_title="Methodology & Documentation", layout="wide")

st.title("Methodology & Documentation")

github_url = "https://github.com/NikHub-2k24/threshold-economic-security"

st.markdown("### Full Documentation & Source")
st.markdown("The GitHub repository contains the complete methodology, source code, experiment definitions, tests, and research notes.")
st.link_button("View Documentation & Source on GitHub \u2192", github_url)

st.markdown("---")

st.markdown("""
### Research Context

**Why cryptographic decentralization does not automatically imply economic decentralization**
A threshold protocol might mathematically guarantee security as long as fewer than $t$ participants are corrupted. However, cryptographic proofs rarely constrain external human behavior. If a rational operator can earn more by accepting an external bribe to defect than by executing the protocol honestly, the system may be economically fragile even if the cryptography remains perfectly intact.

**How threshold systems depend on participant behavior**
The success of a threshold service requires at least $t$ participants to be both available and honest. Their choice to contribute depends on a complex interplay of rewards, execution costs, risk preferences, baseline reliability, and the potential for lost collateral. 

**Individual incentive compatibility vs Coalition stability**
- *Individual incentive compatibility (Nash equilibrium)* ensures that no single operator has a reason to deviate *alone*. 
- *Coalition stability* ensures that no group of operators can coordinate a joint deviation that leaves all of them strictly better off. A protocol might be Nash-stable but extremely vulnerable if just two operators collude.

**Perturbation by external incentives**
An attacker (or smart contract) can offer external incentives to induce deviation. This tool searches for the exact threshold at which these bribes successfully perturb the equilibrium, causing the honest strategy to collapse.

**Service disruption vs Behavioral deviation**
- *Behavioral deviation* means participants are financially incentivized to change their behavior (e.g., $1$ participant defects). 
- *Service disruption* means enough participants deviate that the service actually drops below its required threshold $t$, causing system failure. 
These are fundamentally different concepts, and an economically secure protocol must protect against the latter.

**The impact of repeated interaction**
Many distributed systems are played repeatedly by the same node operators. A deviation that looks highly profitable in a one-shot game might become irrational if it triggers permanent retaliation (a "grim trigger") from the rest of the network, destroying future expected rewards.

**The Conceptual Chain**
`Threshold design` $\\rightarrow$ `participant incentives` $\\rightarrow$ `unilateral deviation` $\\rightarrow$ `coalition deviation` $\\rightarrow$ `external incentives` $\\rightarrow$ `service disruption`
""")

st.markdown("---")

st.markdown("""
### How to Read the Results

**Pure-strategy Nash equilibrium**
- **Mathematical Meaning**: Evaluates if any single participant can strictly improve their utility by unilaterally deviating from the baseline profile (usually `honest`), assuming external bribes are 0.
- **YES/NO Meaning**: A YES means no individual has an incentive to attack alone.
- **What it does NOT mean**: It does NOT mean the protocol is secure against collusion or bribery.
- **Example**: "YES" means the protocol's internal rewards and penalties successfully align individual incentives.

**Strict coalition stability**
- **Mathematical Meaning**: Evaluates if any coalition of participants can coordinate a joint deviation such that every member of the coalition strictly increases their utility, assuming external bribes are 0.
- **YES/NO Meaning**: A YES means the protocol is secure against internal, unbribed collusion.
- **What it does NOT mean**: It does NOT mean the protocol is secure against external attacker bribes.

**Baseline service-failure probability**
- **Mathematical Meaning**: The probability that the service fails purely due to natural unreliability (participants being unavailable according to their individual Bernoulli probabilities), before any strategic defection.
- **Meaning**: Establishes the expected baseline downtime of the network.

**B_behavioral***
- **Mathematical Meaning**: The absolute minimum external incentive required to induce a coalition to execute *any* profitable joint deviation.
- **Meaning**: The cheapest price to corrupt the system's intended behavior.
- **What it does NOT mean**: $B_{behavioral}^*$ $\\neq$ protocol failure! Defection might not drop active participants below $t$.

**B_service***
- **Mathematical Meaning**: The absolute minimum external incentive required to induce a coalition to execute a joint deviation that strictly increases the probability of threshold service failure.
- **Meaning**: The economic cost to successfully attack/halt the network.
- **What it does NOT mean**: It does not prove real-world cryptographic security, as it is bounded by the abstracted model parameters.

**Reservation price**
- **Mathematical Meaning**: The minimum bribe required for a specific individual participant to join a coalition deviation. It is exactly the difference between their honest utility and their deviation utility.

**Repeated-game sustainability**
- **Mathematical Meaning**: Evaluates if the honest profile can be sustained infinitely using a Grim-Trigger strategy (reverting to a Nash punishment profile upon deviation), given a discount factor $\\delta$.
- **Meaning**: Shows if long-term relationships secure the network even when short-term bribery is profitable.
""")

st.markdown("---")

st.markdown("""
### Research Questions

The Threshold Economic Security Lab is designed to explore open questions, including:

- When does increasing the threshold improve economic robustness versus reducing availability?
- Can a threshold system be Nash-stable but coalition-unstable?
- How does collateral affect the cost of a profitable service-disrupting coalition?
- How does participant heterogeneity change coalition formation?
- How sensitive are results to detection probability?
- How does reliability interact with threshold selection?
- When does repeated interaction make cooperation sustainable?
- How different are behavioral and service-failure destabilization thresholds?
- How much does an external incentive change the stability of a threshold system?
- Which parameter combinations produce the largest gap between individual and coalition stability?
""")

st.markdown("---")
st.markdown("### Base Methodology")
st.markdown("""
### Base Actions
Participants choose a base strategy from exactly: `{honest, abstain, defect}`.
- **honest**: Contributes 1 unit when available. Pays `cost_i`, receives `reward_i` on success. No detection/slashing.
- **abstain**: Contributes 0. Pays 0, receives 0. Not slashable by default.
- **defect**: Contributes 0. Pays 0, receives 0. Detected with `detection_probability` and loses `collateral_i`. 

### Utility Function
$M_i(s) = P(\\text{success} \mid s) \cdot \\text{reward}_i(s_i) - \\text{cost}_i(s_i) - P(\\text{detected} \mid s) \cdot \\text{slash}_i(s_i) + \\text{external\\_payment}_i$

$U_i(s) = M_i(s) - \\rho_i \cdot Var_i(\\text{payoff})$
""")

st.markdown("---")
st.link_button("View Documentation & Source on GitHub \u2192", github_url)
