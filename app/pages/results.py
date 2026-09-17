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
st.markdown(f"**Risk Mode**: {'Risk-adjusted' if res.get('risk_aversion', 0)>0 else 'Risk-neutral'}")
st.markdown(f"**Detection probability (defect)**: {res.get('detection_probability_defect', 1.0)}")
st.markdown(f"**Payment Rule**: {res.get('split_rule')}")

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
            
    # Auditable breakdown for Service Failure
    if isinstance(b_serv, float) and "service_details" in res and res["service_details"]:
        details = res["service_details"]
        baseline_fail = 1.0 - res.get("p_success", 1.0)
        dev_fail = 1.0 - details.get("dev_p_success", 1.0)
        st.subheader("Auditable Breakdown (Service Failure)")
        st.write(f"- **Baseline service-failure probability**: {baseline_fail:.4f}")
        st.write(f"- **Service-failure probability after deviation**: {dev_fail:.4f}")
        st.write(f"- **Incremental service-failure probability**: {dev_fail - baseline_fail:.4f}")
        st.write(f"- **Relevant coalition**: {details.get('coalition')}")
        st.write(f"- **Relevant joint deviation**: {[str(s).split('.')[-1] for s in details.get('joint_deviation', [])]}")
        st.write(f"- **Reservation prices**: {[round(r,4) for r in details.get('reservation_prices', [])]}")
            
st.header("REPEATED GAME")
if res.get("repeated_computable"):
    st.metric("Grim-trigger sustainability", "SUSTAINABLE" if res.get("repeated_sustainable") else "NOT SUSTAINABLE")
    st.write(f"Punishment profile: {res.get('punishment_profile')}")
else:
    st.write("Grim-trigger sustainability calculation is not computable under the v1 model.")

st.header("WHY DID THE SYSTEM PRODUCE THIS RESULT?")
if res.get("result_type") == "Enumerated":
    if not res.get("nash_equilibrium"):
        st.write("The honest profile is not a pure-strategy Nash equilibrium because at least one participant obtains a higher expected utility by unilaterally deviating from honest under the configured assumptions.")
    else:
        st.write("The honest profile is a pure-strategy Nash equilibrium. No participant can unilaterally deviate for a strictly higher expected utility.")
        
    if not res.get("coalition_stable"):
        st.write("The honest profile lacks strict coalition stability because there exists a coalition that can jointly deviate to strictly increase every member's utility without external bribes.")
        
    if isinstance(b_serv, float) and b_serv > 0:
        st.write(f"A service-failure destabilization requires an infimum external incentive of {b_serv:.4f} under the {res.get('split_rule')} rule. An attacker offering strictly greater than this amount can induce a rational coalition to fail the service.")

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

## Open Questions
[insufficient data to conclude]
"""
st.download_button("Download Research Report", data=report, file_name="threshold_fairness_lab_report.md", mime="text/markdown")
