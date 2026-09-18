import streamlit as st
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from experiments.experiment_runner import run_experiment

st.set_page_config(page_title="Experiment Builder", layout="wide")
st.title("Experiment Builder")

st.markdown("Configure the parameters for the threshold service game. Default ranges are experimental defaults, not empirical claims.")

presets = {
    "Baseline Threshold": {
        "desc": "Baseline Threshold \u2014 Standard configuration for studying general stability.",
        "vals": {"n": 5, "t": 3, "reward": 10.0, "cost": 2.0, "collateral": 10.0, "rel": 1.0, "risk": 0.0, "dpd": 1.0, "dpa": 0.0, "rule": "attacker_optimal"}
    },
    "External Incentive Sweep": {
        "desc": "External Incentive Sweep \u2014 Low collateral and higher costs to expose vulnerability to bribery.",
        "vals": {"n": 5, "t": 3, "reward": 8.0, "cost": 4.0, "collateral": 2.0, "rel": 1.0, "risk": 0.0, "dpd": 1.0, "dpa": 0.0, "rule": "attacker_optimal"}
    },
    "Collateral Sensitivity": {
        "desc": "Collateral Sensitivity \u2014 Examine how massive collateral changes the incentive required for profitable deviation.",
        "vals": {"n": 5, "t": 4, "reward": 10.0, "cost": 1.0, "collateral": 50.0, "rel": 1.0, "risk": 0.0, "dpd": 0.8, "dpa": 0.0, "rule": "attacker_optimal"}
    },
    "Reliability vs Threshold": {
        "desc": "Reliability vs Threshold \u2014 Lower baseline reliability requiring higher n/t ratio balancing.",
        "vals": {"n": 7, "t": 5, "reward": 15.0, "cost": 3.0, "collateral": 10.0, "rel": 0.85, "risk": 0.1, "dpd": 1.0, "dpa": 0.0, "rule": "equal_split"}
    },
    "Coalition Size": {
        "desc": "Coalition Size \u2014 Equal split rule forcing attackers to pay identical bribes across large coalitions.",
        "vals": {"n": 8, "t": 6, "reward": 5.0, "cost": 1.0, "collateral": 5.0, "rel": 1.0, "risk": 0.0, "dpd": 1.0, "dpa": 0.0, "rule": "equal_split"}
    },
    "Repeated-Game Sustainability": {
        "desc": "Repeated-Game Sustainability \u2014 Low immediate rewards but high potential future losses if Grim-Trigger is activated.",
        "vals": {"n": 3, "t": 2, "reward": 2.0, "cost": 1.0, "collateral": 0.0, "rel": 1.0, "risk": 0.0, "dpd": 0.0, "dpa": 0.0, "rule": "attacker_optimal"}
    },
    "Custom": {
        "desc": "Custom \u2014 Manually define your research parameters.",
        "vals": None
    }
}

st.header("Research Presets")
selected_preset = st.selectbox("Select a Preset", list(presets.keys()))
st.info(presets[selected_preset]["desc"])

# Apply preset if changed
if "last_preset" not in st.session_state or st.session_state["last_preset"] != selected_preset:
    st.session_state["last_preset"] = selected_preset
    if presets[selected_preset]["vals"] is not None:
        v = presets[selected_preset]["vals"]
        st.session_state["n"] = v["n"]
        st.session_state["t"] = v["t"]
        st.session_state["reward"] = v["reward"]
        st.session_state["cost"] = v["cost"]
        st.session_state["collateral"] = v["collateral"]
        st.session_state["reliability"] = v["rel"]
        st.session_state["risk_aversion"] = v["risk"]
        st.session_state["dpd"] = v["dpd"]
        st.session_state["dpa"] = v["dpa"]
        st.session_state["rule"] = v["rule"]

def get_ss(key, default):
    return st.session_state.get(key, default)

st.header("Protocol")
col1, col2 = st.columns(2)
with col1:
    n = st.number_input("n (Participants)", min_value=1, max_value=20, value=get_ss("n", 3))
with col2:
    t = st.number_input("t (Threshold)", min_value=1, max_value=n, value=get_ss("t", 2))

st.header("Global Assumptions")
col3, col4 = st.columns(2)
with col3:
    detection_probability_defect = st.slider("Detection Probability (Defect)", 0.0, 1.0, get_ss("dpd", 1.0))
    detection_probability_abstain = st.slider("Detection Probability (Abstain)", 0.0, 1.0, get_ss("dpa", 0.0))
with col4:
    rules = ["attacker_optimal", "equal_split"]
    default_rule = get_ss("rule", "attacker_optimal")
    idx = rules.index(default_rule) if default_rule in rules else 0
    split_rule = st.selectbox("Payment Rule", rules, index=idx)

st.header("Participants")
symmetric = st.checkbox("Symmetric Participants", value=True)

if symmetric:
    col5, col6, col7 = st.columns(3)
    with col5:
        reward = st.number_input("Honest Reward", value=get_ss("reward", 10.0))
        cost = st.number_input("Cost", value=get_ss("cost", 2.0))
    with col6:
        collateral = st.number_input("Collateral", value=get_ss("collateral", 5.0))
        reliability = st.slider("Reliability (1 - failure prob)", 0.0, 1.0, get_ss("reliability", 1.0))
    with col7:
        risk_aversion = st.number_input("Risk Aversion (rho)", value=get_ss("risk_aversion", 0.0))
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
        "split_rule": split_rule,
        "delta": 0.9  # Default repeated game delta
    }
    
    with st.spinner("Computing..."):
        res = run_experiment(cfg)
        st.session_state["latest_result"] = res
        st.success("Experiment completed. Go to Results page.")
