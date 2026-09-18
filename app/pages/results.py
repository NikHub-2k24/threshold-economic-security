import streamlit as st
import os, sys

st.set_page_config(page_title="Results", layout="wide")
st.title("Results")

if "latest_result" not in st.session_state:
    st.warning("No experiment data found. Please run an experiment in the Experiment Builder.")
    st.stop()

res = st.session_state["latest_result"]

st.markdown(f"**Result type**: {res.get('result_type')}")
st.markdown(f"**n**: {res.get('n')}, **t**: {res.get('t')}")

st.header("BASELINE STAGE GAME")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Pure-strategy Nash equilibrium", "YES" if res.get("nash_equilibrium") == True else ("NO" if res.get("nash_equilibrium") == False else "NOT COMPUTED"))
with col2:
    st.metric("Strict coalition stability", "YES" if res.get("coalition_stable") == True else ("NO" if res.get("coalition_stable") == False else "NOT COMPUTED"))
with col3:
    st.metric("Baseline service-failure probability", f"{1.0 - res.get('p_success', 1.0):.4f}")

st.header("EXTERNAL-INCENTIVE ANALYSIS")
b_behav = res.get("b_behavioral_star")
b_serv = res.get("b_service_star")

if b_behav is None and res.get("result_type") == "Enumerated":
    if res.get("coalition_stable") == False:
        st.error("Honest profile is intrinsically unstable under the baseline game; therefore no external incentive is required to induce a profitable deviation.")
        st.metric("Behavioral destabilization threshold B_behavioral*", "0.0")
        st.metric("Service-failure destabilization threshold B_service*", "0.0")
elif res.get("result_type") == "Simulated":
    st.info("Exact equilibrium analysis not computed for n > 8.")
else:
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Behavioral destabilization threshold B_behavioral*", f"{b_behav:.4f}" if isinstance(b_behav, float) else "NOT COMPUTED")
    with col5:
        if isinstance(b_serv, float):
            st.metric("Service-failure destabilization threshold B_service*", f"{b_serv:.4f}")
        else:
            st.metric("Service-failure threshold", "not reachable under current model")

st.header("REPEATED GAME")
if res.get("repeated_computable"):
    st.metric("Grim-trigger sustainability", "SUSTAINABLE" if res.get("repeated_sustainable") else "NOT SUSTAINABLE")
    st.write(f"Punishment profile: {res.get('punishment_profile')}")
else:
    st.write("Grim-trigger sustainability calculation is not computable under the current model constraints.")

st.markdown("---")

st.header("INTERPRETATION")
if res.get("result_type") == "Enumerated":
    interp = "The baseline honest profile is "
    if res.get("nash_equilibrium"):
        interp += "a pure-strategy Nash equilibrium "
    else:
        interp += "NOT a pure-strategy Nash equilibrium "
        
    if res.get("coalition_stable"):
        interp += "and is strictly coalition-stable under the configured assumptions. "
    else:
        interp += "but lacks strict coalition stability under the configured assumptions. "
        
    if b_behav is None and res.get("coalition_stable") == False:
        interp += "Because the system is intrinsically unstable, no external incentive is required to induce a profitable deviation."
    else:
        if isinstance(b_serv, float):
            interp += f"A service-disrupting coalition would require an external incentive with infimum B_service* = {b_serv:.4f}. "
        else:
            interp += "No feasible coalition/deviation under the configured model can cause service failure. "
            
    if res.get("repeated_computable"):
        if res.get("repeated_sustainable"):
            interp += "However, under infinite-horizon repeated interaction, the honest profile can be sustained by a grim-trigger strategy, deterring short-term deviations."
        else:
            interp += "Under infinite-horizon repeated interaction, the honest profile cannot be sustained, meaning long-term relationships do not provide sufficient deterrent."
            
    st.write(interp)

st.markdown("---")

if isinstance(b_serv, float) and "service_details" in res and res["service_details"]:
    with st.expander("View calculation details", expanded=False):
        details = res["service_details"]
        baseline_fail = 1.0 - res.get("p_success", 1.0)
        dev_fail = 1.0 - details.get("dev_p_success", 1.0)
        
        st.markdown(f"**Relevant coalition**: {details.get('coalition')}")
        st.markdown(f"**Relevant joint deviation**: {[str(s).split('.')[-1] for s in details.get('joint_deviation', [])]}")
        st.markdown(f"**Reservation prices**: {[round(r,4) for r in details.get('reservation_prices', [])]}")
        st.markdown(f"**Baseline failure probability**: {baseline_fail:.4f}")
        st.markdown(f"**Post-deviation failure probability**: {dev_fail:.4f}")
        st.markdown(f"**Incremental failure probability**: {dev_fail - baseline_fail:.4f}")
        st.markdown(f"**Payment rule**: {res.get('split_rule')}")
        st.markdown(f"**Risk mode**: {'Risk-adjusted' if res.get('risk_aversion', 0)>0 else 'Risk-neutral'}")
        st.markdown(f"**Detection probability (defect)**: {res.get('detection_probability_defect', 1.0)}")
        st.markdown(f"**Result type**: {res.get('result_type')}")

st.header("RESEARCH EXPORT")
st.markdown("Download a Markdown report summarizing this experiment.")
report = f"""# Research Report

## Question
Under what external incentive regimes do threshold cryptographic services cease to be economically fair?

## Model
- n={res.get('n')}, t={res.get('t')}
- Payment Rule: {res.get('split_rule')}

## Results
- Pure-strategy Nash equilibrium: {'YES' if res.get('nash_equilibrium')==True else 'NO'}
- Strict coalition stability: {'YES' if res.get('coalition_stable')==True else 'NO'}
- B_behavioral*: {b_behav if b_behav is not None else 'N/A'}
- B_service*: {b_serv if b_serv is not None else 'N/A'}

## Interpretation
{interp if res.get("result_type") == "Enumerated" else "Simulated result; exact interpretation omitted."}
"""
st.download_button("Download Research Report", data=report, file_name="threshold_economic_security_report.md", mime="text/markdown")
