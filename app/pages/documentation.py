import streamlit as st

st.set_page_config(page_title="Methodology & Documentation", layout="wide")
st.title("Methodology & Documentation")

st.markdown("""
### Core Purpose
The tool is an abstract research model of economic incentives in threshold services. It does not prove real-world cryptographic security and does not model actual cryptographic compromise in v1.

### Base Actions
Participants choose a base strategy from exactly: `{honest, abstain, defect}`.
- **honest**: Contributes 1 unit when available. Pays `cost_i`, receives `reward_i` on success. No detection/slashing.
- **abstain**: Contributes 0. Pays 0, receives 0. Not slashable by default.
- **defect**: Contributes 0. Pays 0, receives 0. Detected with `detection_probability` and loses `collateral_i`. 

### Threshold Service
Service succeeds iff the number of available participants playing **honest** is $\ge t$.

### Utility Function
$M_i(s) = P(\text{success} \mid s) \cdot \text{reward}_i(s_i) - \text{cost}_i(s_i) - P(\text{detected} \mid s) \cdot \text{slash}_i(s_i) + \text{external\_payment}_i$

$U_i(s) = M_i(s) - \rho_i \cdot Var_i(\text{payoff})$

### Equilibria & Stability
- **Pure-strategy Nash equilibrium**: No single participant has a strict profitable unilateral deviation in the unbribed game.
- **Strict coalition stability**: No coalition $C$ has a joint deviation where every member strictly gains in the unbribed game.

### Destabilization Thresholds
- **$B_{behavioral}^*$**: Infimum required for any profitable coalition deviation.
- **$B_{service}^*$**: Infimum required for a coalition deviation that causes service failure.
- Rules: **attacker_optimal** ($B^* = \sum r_i$) and **equal_split** ($B^* = |C| \cdot \max(r_i)$).

### Repeated Game
- Infinite-horizon grim-trigger sustainability check evaluated against an explicit pure-strategy Nash punishment profile.
""")
