import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import csv
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from experiments.experiment_runner import run_experiment

st.set_page_config(page_title="Graphs", layout="wide")
st.title("Graphs & Visualizations")

data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'results.csv')

def run_default_sweep():
    results = []
    
    total_steps = sum(1 for n in range(3, 9) for t in range(2, n + 1))
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    step = 0
    for n in range(3, 9):
        for t in range(2, n + 1):
            status_text.text(f"Computing exact enumeration for n={n}, t={t}...")
            cfg = {
                "n": n, "t": t, "reward": 10.0, "cost": 2.0, "collateral": 5.0, 
                "reliability": 1.0, "risk_aversion": 0.0,
                "detection_probability_defect": 1.0, "detection_probability_abstain": 0.0,
                "split_rule": "attacker_optimal",
                "delta": 0.9
            }
            results.append(run_experiment(cfg))
            step += 1
            progress_bar.progress(step / total_steps)
            
    status_text.text("Saving results...")
    
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    keys = results[0].keys()
    with open(data_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
        
    progress_bar.empty()
    status_text.empty()
    st.success("Default research sweep complete! Data generated.")
    time.sleep(1)
    st.rerun()

st.markdown("Visualizations require experiment sweep data.")
if st.button("Run Default Research Sweep"):
    run_default_sweep()

if not os.path.exists(data_path):
    st.warning("Insufficient experiment data for this visualization. Run the default research sweep above, or use the CLI.")
    st.stop()

df = pd.read_csv(data_path)

if len(df) < 3 or len(df['n'].unique()) < 2:
    st.warning("Insufficient experiment data for this visualization. Run the default research sweep above, or use the CLI.")
    st.stop()

st.header("Threshold Matrix (x=n, y=t)")
if 'n' in df.columns and 't' in df.columns and 'b_service_star' in df.columns:
    df_exact = df[df['result_type'] == 'Enumerated'].copy()
    df_exact['b_service_star'] = pd.to_numeric(df_exact['b_service_star'], errors='coerce')
    if len(df_exact['n'].unique()) > 1:
        pivot = df_exact.pivot_table(index='t', columns='n', values='b_service_star')
        fig = px.imshow(pivot, text_auto=True, title="Minimum Destabilizing Incentive (B_service_star) [Enumerated]", origin="lower")
        st.plotly_chart(fig)
    else:
        st.write("Insufficient exact enumeration data available for matrix. Run a parameter sweep over n and t.")
        
st.header("Reliability / Service-Failure Frontier")
if 't' in df.columns and 'p_success' in df.columns:
    df_frontier = df.copy()
    if len(df_frontier['t'].unique()) > 1:
        fig = px.line(df_frontier, x='t', y='p_success', color='n', markers=True, title="Service Availability by Threshold (Simulated/Enumerated)")
        st.plotly_chart(fig)
    else:
        st.write("Insufficient data for frontier visualization. Run a parameter sweep.")
