import streamlit as st
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from experiments.experiment_runner import run_experiment

st.set_page_config(page_title="Experiment Builder", layout="wide")
st.title("Experiment Builder")

st.markdown("Configure the parameters for the threshold service game. Default ranges are experimental defaults, not empirical claims.")

st.header("Protocol")
col1, col2 = st.columns(2)
with col1:
    n = st.number_input("n (Participants)", min_value=1, max_value=20, value=3)
with col2:
    t = st.number_input("t (Threshold)", min_value=1, max_value=n, value=2)

st.header("Global Assumptions")
col3, col4 = st.columns(2)
with col3:
    detection_probability_defect = st.slider("Detection Probability (Defect)", 0.0, 1.0, 1.0)
    detection_probability_abstain = st.slider("Detection Probability (Abstain)", 0.0, 1.0, 0.0)
with col4:
    split_rule = st.selectbox("Payment Rule", ["attacker_optimal", "equal_split"])

st.header("Participants")
symmetric = st.checkbox("Symmetric Participants", value=True)

if symmetric:
    col5, col6, col7 = st.columns(3)
    with col5:
        reward = st.number_input("Honest Reward", value=10.0)
        cost = st.number_input("Cost", value=2.0)
    with col6:
        collateral = st.number_input("Collateral", value=5.0)
        reliability = st.slider("Reliability (1 - failure prob)", 0.0, 1.0, 1.0)
    with col7:
        risk_aversion = st.number_input("Risk Aversion (rho)", value=0.0)
else:
    st.error("Heterogeneous configuration UI not fully scaffolded in this quick demo.")
    reward = 10.0; cost = 2.0; collateral = 5.0; reliability = 1.0; risk_aversion = 0.0
    
if st.button("Run Exact Experiment" if n <= 8 else "Run Simulation (n>8)"):
    cfg = {
        "n": n,
        "t": t,
        "reward": reward,
        "cost": cost,
        "collateral": collateral,
        "reliability": reliability,
        "risk_aversion": risk_aversion,
        "detection_probability_defect": detection_probability_defect,
        "detection_probability_abstain": detection_probability_abstain,
        "split_rule": split_rule
    }
    
    with st.spinner("Computing..."):
        res = run_experiment(cfg)
        st.session_state["latest_result"] = res
        st.success("Experiment completed. Go to Results page.")
