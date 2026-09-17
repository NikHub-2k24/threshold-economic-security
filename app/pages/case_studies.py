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
st.title("Case Studies")

st.markdown("Abstract, simplified models inspired by research problems. Computed locally with no external chain data.")

study = st.selectbox("Select Case Study", [
    "Threshold service payment on a UTXO blockchain",
    "Atomic exchange with user/miner collusion",
    "Threshold oracle service",
    "Distributed randomness service"
])

if study == "Threshold service payment on a UTXO blockchain":
    cfg = get_utxo_threshold_payment_config()
elif study == "Atomic exchange with user/miner collusion":
    cfg = get_atomic_exchange_collusion_config()
elif study == "Threshold oracle service":
    cfg = get_threshold_oracle_config()
elif study == "Distributed randomness service":
    cfg = get_distributed_randomness_config()

st.json(cfg)

if st.button("Run Case Study"):
    res = run_experiment(cfg)
    st.session_state["latest_result"] = res
    st.success("Case study computed. Go to Results page.")
