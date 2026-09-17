import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from experiments.experiment_runner import run_experiment

st.set_page_config(page_title="Threshold Fairness Lab", layout="wide")

st.title("Threshold Fairness Lab")
st.subheader("When is a cryptographically decentralized service actually economically decentralized?")

st.markdown("""
A 4-of-7 threshold service may resist cryptographic compromise while still becoming economically unstable if an external actor can make deviation profitable.

**Threshold Fairness Lab lets researchers test that boundary.**
""")

st.write("---")

st.markdown("### Quick Example")
st.markdown("4-of-7, reward 1.0, collateral 0.2, external incentive 0.65")
if st.button("Run experiment"):
    cfg = {
        "n": 7,
        "t": 4,
        "reward": 1.0,
        "cost": 0.0,
        "collateral": 0.2,
        "reliability": 1.0
    }
    res = run_experiment(cfg)
    b_star = res.get("b_behavioral_star")
    
    if b_star is not None and 0.65 > b_star:
        st.error(f"Profitable coalition deviation detected at external incentive = 0.65 (Threshold B* = {b_star:.4f}).")
    else:
        st.success(f"No profitable deviation at external incentive = 0.65 under the configured model (Threshold B* = {b_star if b_star else 'N/A'}).")
        
    with st.expander("View raw experiment output"):
        st.json(res)
