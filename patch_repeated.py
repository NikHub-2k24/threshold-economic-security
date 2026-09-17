import re

with open("models/repeated_game.py", "r") as f:
    content = f.read()

replacement = """def find_pure_strategy_nash_equilibria(game: Game) -> List[Tuple[Strategy, ...]]:
    n = len(game.participants)
    
    # Fast paths: check obvious punishment profiles first
    candidates = [
        tuple([Strategy.ABSTAIN] * n),
        tuple([Strategy.DEFECT] * n)
    ]
    for c in candidates:
        if is_pure_strategy_nash_equilibrium(game, c):
            return [c]
            
    # Fallback to full enumeration
    profiles = get_all_profiles(n)
    return [p for p in profiles if is_pure_strategy_nash_equilibrium(game, p)]"""

content = re.sub(r'def find_pure_strategy_nash_equilibria\(game: Game\) -> List\[Tuple\[Strategy, \.\.\.\]\]:.*?return \[p for p in profiles if is_pure_strategy_nash_equilibrium\(game, p\)\]', replacement, content, flags=re.DOTALL)

with open("models/repeated_game.py", "w") as f:
    f.write(content)
