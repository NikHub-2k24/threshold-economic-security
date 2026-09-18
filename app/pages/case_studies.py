import streamlit as st
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from protocols.case_studies import (
    get_utxo_threshold_payment_config,
    get_atomic_exchange_collusion_config,
    get_threshold_oracle_config,
    get_distributed_randomness_config
)
from experiments.experiment_runner import run_experiment

st.set_page_config(page_title="Case Studies", layout="wide")
st.title("Protocol Case Studies")

st.markdown("These case studies provide pre-configured parameter sets representing abstract models of threshold systems. They are **educational scaffolding only** and should not be interpreted as exact simulations of real-world production networks.")

study = st.selectbox("Select Case Study", [
    "Threshold service payment on a UTXO-style blockchain",
    "Atomic exchange with user/miner collusion",
    "Threshold oracle service",
    "Distributed randomness service"
])

if study == "Threshold service payment on a UTXO-style blockchain":
    cfg = get_utxo_threshold_payment_config()
    st.markdown("---")
    st.markdown('''**Research Question**: How does standard cost vs. reward scaling affect individual incentive compatibility in a simple payment threshold?
    
**What This Model Represents**: A straightforward threshold signature where participants receive a fixed reward for co-signing a valid transaction and pay a fixed computational/network cost.
    
**What Is Abstracted Away**: Dynamic fee markets, mempool mechanics, partial signatures, and real-time token valuation.
    
**Key Variables**: `reward`, `cost`, `t`.
    
**What to Experiment With**: Try lowering the reward to approach the cost. At what point does `abstain` become a strict Nash equilibrium due to availability uncertainty?
    
**How to Interpret the Result**: Look at the baseline stability. If it fails, the protocol isn't paying enough to overcome the execution cost risk.
    
**Limitations**: Assumes identical operators and static rewards.''')
    
elif study == "Atomic exchange with user/miner collusion":
    cfg = get_atomic_exchange_collusion_config()
    st.markdown("---")
    st.markdown('''**Research Question**: How does slashable collateral change the economic viability of coalition attacks?
    
**What This Model Represents**: An exchange mechanism where participants post collateral. If they defect (e.g., equivocate or withhold signatures), they can be caught and slashed.
    
**What Is Abstracted Away**: Cryptographic evidence generation, smart contract slashing resolution times, and the time value of locked capital.
    
**Key Variables**: `collateral`, `detection_probability_defect`.
    
**What to Experiment With**: Drop the `detection_probability_defect` to 0.5. How much does `B_service*` drop? 
    
**How to Interpret the Result**: The $B_{service}^*$ threshold directly measures the financial wall an attacker must climb to override the collateral deterrent.
    
**Limitations**: Perfect enforcement assumed when detected; no legal or out-of-band consequences modeled.''')
    
elif study == "Threshold oracle service":
    cfg = get_threshold_oracle_config()
    st.markdown("---")
    st.markdown('''**Research Question**: How does participant heterogeneity in reliability and risk affect the vulnerability of a committee?
    
**What This Model Represents**: An oracle network where some operators run enterprise-grade infrastructure (high reliability) and others run hobbyist setups (lower reliability and higher risk aversion).
    
**What Is Abstracted Away**: The data source quality, off-chain aggregation delays, and specific oracle reporting mechanics.
    
**Key Variables**: `reliability` (heterogeneous), `risk_aversion`.
    
**What to Experiment With**: Change the bribery split rule to `attacker_optimal`. Does the attacker target the highly reliable nodes or the hobbyists?
    
**How to Interpret the Result**: A $B_{service}^*=0$ means the heterogeneous setup is already intrinsically unstable. Otherwise, look at the coalition makeup in the calculation details.
    
**Limitations**: Risk aversion is modeled linearly against variance; actual operator risk profiles may be highly non-linear.''')
    
elif study == "Distributed randomness service":
    cfg = get_distributed_randomness_config()
    st.markdown("---")
    st.markdown('''**Research Question**: When is a high-availability requirement economically self-defeating?
    
**What This Model Represents**: A distributed randomness beacon requiring a very high threshold (e.g., $t=7$ out of $n=8$) to ensure liveness, making the protocol fragile to minor abstention.
    
**What Is Abstracted Away**: BLS signature aggregation, DKG (Distributed Key Generation) phases, and network latency.
    
**Key Variables**: $t$ (set close to $n$), `detection_probability_abstain`.
    
**What to Experiment With**: Increase $n$ without increasing $t$. Watch how the probability of service success recovers.
    
**How to Interpret the Result**: Notice how small the incremental failure probability might be if the baseline failure probability is already high.
    
**Limitations**: Abstention is treated as a static strategy rather than an intermittent network failure.''')

st.markdown("---")
st.json(cfg)

if st.button("Run Case Study"):
    res = run_experiment(cfg)
    st.session_state["latest_result"] = res
    st.success("Case study computed. Go to Results page.")
