import pytest
from core.strategies import Strategy
from core.participants import Participant
from core.protocol import Protocol
from core.adversary import AdversaryConfig
from core.game import Game
from core.equilibrium import (
    is_pure_strategy_nash_equilibrium,
    is_strict_coalition_stable,
    get_destabilization_thresholds
)

def test_case_1_stable():
    """
    Case 1: Honest Nash eq = YES, Coalition stability = YES
    n=3, t=2. reward=10, cost=2, collateral=5. reliability=1.0
    Honest payoff: 1.0 * 10 - 2 = 8.
    Unilateral abstain: 2 honest left (success). Payoff = 0. (0 < 8) -> Nash=YES
    Coalition (2) abstain: 1 honest left (fail). Payoff = 0. (0 < 8) -> Stable=YES
    """
    protocol = Protocol(n=3, t=2, detection_probability_defect=1.0)
    participants = [Participant(id=i, cost=2.0, reward=10.0, collateral=5.0, reliability=1.0) for i in range(3)]
    game = Game(protocol, participants, AdversaryConfig())
    profile = (Strategy.HONEST, Strategy.HONEST, Strategy.HONEST)
    
    assert is_pure_strategy_nash_equilibrium(game, profile) == True
    assert is_strict_coalition_stable(game, profile) == True

def test_case_2_unstable_coalition():
    """
    Case 2: Honest Nash eq = YES, Coalition stability = NO
    n=3, t=2. reward=10, cost=2, collateral=5. reliability=1.0
    Wait, to make it coalition unstable but Nash stable:
    If 1 abstains, success continues, gets 0. (Nash stable if reward-cost > 0)
    If 2 abstain, success fails. Payoff = 0. This doesn't make them gain.
    What if the service is a free rider problem?
    Actually, to make coalition unstable, they need to GAIN.
    If 2 people defect/abstain, they can only get 0. Since honest gets 8, they won't.
    What if cost > reward? Then honest payoff < 0.
    If cost=10, reward=5.
    Honest payoff: 1 * 5 - 10 = -5.
    If 1 abstains, success continues! Payoff = 0. (0 > -5) -> Nash=NO.
    So this breaks Nash too.
    How to have Nash=YES but Coalition=NO?
    Need U_i(honest) > U_i(unilateral dev), but U_i(joint dev) > U_i(honest).
    If I unilateral abstain -> service fails! So I must be critical.
    Let n=3, t=3. (Everyone is critical).
    reward=10, cost=2.
    Honest payoff: 10 - 2 = 8.
    Unilateral abstain -> 2 honest, fails (t=3). Payoff = 0. (0 < 8) -> Nash=YES.
    Joint abstain -> fails. Payoff = 0.
    Since 0 < 8, still coalition stable.
    How to get Coalition NO?
    Maybe through external bribery? No, the intrinsic game must be unstable.
    In threshold public goods, if cost > 0 and reward > cost, and you are critical, you want to participate.
    If you are NOT critical, you want to free ride.
    If n=3, t=2.
    Profile (H, H, H): 3 honest.
    Unilateral abstain: 2 honest, success. Payoff = 0.
    Wait! If I abstain, I get 0. But I save cost!
    Ah! "honest: receives reward_i if service succeeds".
    Wait, if I abstain, do I get the reward if service succeeds?
    The spec says:
    "abstain: ... receives no honest reward"
    Ah, so you ONLY get the reward if you play honest!
    Then you CANNOT free ride on the reward!
    Let's check the spec:
    "reward_i(s_i) = reward_i if s_i = honest, else 0 (the deviating participant does not collect the honest reward)."
    Yes! So there is NO free riding on the reward!
    If there is no free riding on the reward, how can a coalition gain by deviating intrinsically?
    Only if honest payoff is negative! But if honest payoff is negative, then unilateral abstain also gives 0, which is > negative, so Nash is NO.
    Is it mathematically possible to have Nash=YES and Coalition=NO with these exact rules?
    Wait. What if reliability < 1?
    If n=3, t=2, reliability=0.5.
    P(success | 3H) = P(X>=2 for B(3, 0.5)) = 0.5.
    U(H|3H) = 0.5 * 10 - 2 = 3.
    If unilateral abstain (2H, 1A):
    P(success | 2H) = P(X>=2 for B(2, 0.5)) = 0.25.
    But if you abstain, you get 0 reward anyway!
    So U(A|2H) = 0.
    Since 0 < 3, Nash = YES.
    What if Coalition of 2 abstains?
    They get 0. 0 < 3.
    So when could they possibly get > 3? Only if they get external bribes, but this is the intrinsic game!
    Wait, what if collateral is NEGATIVE? No.
    What if risk aversion makes honest < 0, but variance of abstain is 0?
    If rho = 10, U(H) = 3 - 10 * Var. Var = 100 * 0.25 = 25. U(H) = 3 - 250 = -247.
    Then unilateral abstain gives U(A) = 0. So Nash = NO.
    Is there ANY case where Nash=YES, Coalition=NO intrinsically?
    Maybe if reward depends on coalition? No, reward is constant.
    Maybe there is no such case in this specific restricted game model without external bribes.
    Wait, the user says "At least one must cover: Honest Nash eq = YES, Coalition stability = NO".
    How? Let's read carefully: "A coalition C is a subset of participants... A coalition deviation must differ from the original profile for at least one member... determine whether external payment can make EVERY coalition member strictly better off."
    Wait, the test requirement is:
    "At least one must cover: honest Nash equilibrium = YES, coalition stability = NO".
    Perhaps they mean *with* external bribery?
    No, "strict coalition stability" is defined on the UNBRIBED game. "Baseline strict coalition stability: YES/NO".
    If it's mathematically impossible for this specific utility function, then I should just set a case where it happens... but how?
    Wait. What if one person plays H and one plays A, and they jointly swap?
    But the baseline profile tested is usually ALL HONEST. "Normally the starting profile is the honest profile."
    Ah, what if the baseline profile is NOT all honest?
    If profile is (H, A, A), n=3, t=1.
    P(success | H,A,A) = 1. U_1(H) = 10 - 2 = 8.
    U_2(A) = 0. U_3(A) = 0.
    Can 2 and 3 jointly deviate to (H, H)?
    If 2 plays H, P(success)=1, U_2(H) = 8. (Unilateral deviation is profitable! So Nash=NO).
    Okay, what if profile is (H, H, H) and cost is negative? No.
    What if detection probability is < 0? No.
    What if `cost_i` is positive, but `reward_i` is 0? Then U(H) < 0, Nash=NO.
    Is there any interaction between players?
    The only interaction is P(success).
    If player i changes from H to A, P(success) goes down.
    Since player i's utility only depends on P(success) if they play H (otherwise it's 0 or negative),
    If they play A or D, their utility is independent of P(success).
    So if U_i(H) >= U_i(A) = 0, they want to play H.
    If EVERYONE has U_i(H) >= 0 under the current profile, then no one wants to unilaterally deviate to A.
    Can a coalition jointly deviate to (A,A) and gain?
    If they deviate to (A,A), they get 0. But they already had U_i(H) >= 0. So they don't strictly gain.
    So if Nash=YES (meaning U_i(H) >= 0 for all i), then ANY joint deviation to A gives 0, which is not > U_i(H).
    What if they deviate to D? Gives <= 0.
    So if Nash=YES, then Coalition Stability MUST be YES for the all-honest profile!
    Wait, is there any case where Nash=YES but Coalition=NO for the all-honest profile?
    No, because actions A and D have utilities that do NOT depend on other players' actions!
    Utility of A is ALWAYS 0. Utility of D is ALWAYS -p*slash.
    Since the utility of deviating is constant, if it's not strictly profitable unilaterally, it CANNOT be strictly profitable jointly!
    Ah! "Utility of A is always 0".
    Wait, what if one player's unilateral deviation lowers P(success) so much that another player's H becomes negative?
    Yes, but the coalition members must ALL strictly gain.
    If player 1 and 2 jointly deviate to (A, A), they both get 0.
    For this to be strictly profitable, they must have had < 0 before.
    But if they had < 0 before, they could just unilaterally deviate to A and get 0!
    So they would have had a unilateral deviation! Thus Nash would be NO.
    Therefore, for the all-honest profile, Nash=YES implies Coalition Stability=YES.
    Wait... is this true?
    Let U_i(s) = P(s)*R - C.
    Unilateral Nash: P(s) * R - C >= 0  => P(s) * R >= C.
    If they jointly deviate to A, they get 0. They only gain if P(s)*R - C < 0, which violates Nash.
    So Coalition Stability = NO (intrinsically) is IMPOSSIBLE if Nash = YES, for the ALL-HONEST profile!
    BUT wait! What if the profile is NOT all-honest?
    Suppose baseline profile is (A, A, A).
    n=2, t=1. R=10, C=8.
    Profile: (A, A). P(success) = 0. U_1 = 0, U_2 = 0.
    Unilateral deviation to H by P1:
    Profile: (H, A). P(success) = 1 (if reliability=1).
    U_1(H) = 10 - 8 = 2.
    Since 2 > 0, unilateral deviation is profitable! So Nash = NO.
    What if reliability is 0.5?
    Profile: (A, A). U = 0.
    Unilateral to H: P(success) = 0.5. U_1(H) = 0.5*10 - 8 = -3.
    Since -3 < 0, Unilateral deviation to H is NOT profitable!
    So Nash = YES for (A, A)!
    What about Coalition deviation?
    Coalition {1, 2} deviates to (H, H).
    P(success | H, H) = 1 - 0.5^2 = 0.75.
    U_i(H) = 0.75 * 10 - 8 = 7.5 - 8 = -0.5. Still < 0.
    What if R=14, C=8, reliability=0.5.
    Unilateral to H: P(success)=0.5. U_1 = 0.5 * 14 - 8 = 7 - 8 = -1.
    Since -1 < 0, Nash = YES for profile (A, A).
    Now Coalition {1, 2} deviates to (H, H).
    P(success | H, H) = 0.75.
    U_i = 0.75 * 14 - 8 = 10.5 - 8 = 2.5.
    Since 2.5 > 0, BOTH members strictly gain!
    So Coalition Stability = NO!
    BINGO!
    Nash = YES, Coalition = NO is possible for profile (A, A) with n=2, t=1, r=14, c=8, rel=0.5.
    Let's use this for Case 2!
    """
    protocol = Protocol(n=2, t=1)
    participants = [Participant(id=i, cost=8.0, reward=14.0, collateral=5.0, reliability=0.5) for i in range(2)]
    game = Game(protocol, participants, AdversaryConfig())
    profile = (Strategy.ABSTAIN, Strategy.ABSTAIN)
    
    assert is_pure_strategy_nash_equilibrium(game, profile) == True
    assert is_strict_coalition_stable(game, profile) == False

def test_case_3_unstable_nash():
    """
    Case 3: Profitable unilateral deviation (Nash = NO)
    n=3, t=2. reward=10, cost=12 (cost > reward).
    Honest payoff < 0. Unilateral deviation to Abstain gives 0.
    """
    protocol = Protocol(n=3, t=2)
    participants = [Participant(id=i, cost=12.0, reward=10.0, collateral=5.0, reliability=1.0) for i in range(3)]
    game = Game(protocol, participants, AdversaryConfig())
    profile = (Strategy.HONEST, Strategy.HONEST, Strategy.HONEST)
    
    assert is_pure_strategy_nash_equilibrium(game, profile) == False
    assert is_strict_coalition_stable(game, profile) == False  # since unilateral implies coalition of 1

def test_case_4_coalition_bribe():
    """
    Case 4: Coalition deviation requiring non-zero external incentive
    n=3, t=2. reward=10, cost=2, collateral=5. rel=1.0
    Honest payoff = 8.
    Coalition of 2 deviates to ABSTAIN.
    Service fails (1 honest left < 2).
    Payoff becomes 0.
    Reservation price for each = 8 - 0 = 8.
    So B* (attacker optimal) = 8 + 8 = 16.
    """
    protocol = Protocol(n=3, t=2)
    participants = [Participant(id=i, cost=2.0, reward=10.0, collateral=5.0, reliability=1.0) for i in range(3)]
    game = Game(protocol, participants, AdversaryConfig())
    profile = (Strategy.HONEST, Strategy.HONEST, Strategy.HONEST)
    
    thresholds = get_destabilization_thresholds(game, profile, split_rule="attacker_optimal")
    
    assert thresholds["intrinsically_stable"] == True
    assert thresholds["b_behavioral_star"] == 8.0  # Wait! Unilateral deviate gives 0. r_i = 8.
    # A single person deviating to ABSTAIN: 2 honest left, service succeeds!
    # Payoff becomes 0. r_i = 8 - 0 = 8. B* = 8.
    # Service doesn't fail! So B_behavioral* = 8.
    # For service to fail, 2 people must deviate. r_1 = 8, r_2 = 8. B* = 16.
    assert thresholds["b_service_star"] == 16.0

def test_case_5_strict_profitability_epsilon():
    """
    Case 5: Verification of B* infimum vs B* + epsilon strict profitability.
    From Case 4, B_service* = 16.0.
    If bribe is exactly 16, they get exactly their reservation price.
    Strict profitability requires B > 16.
    We just verify the infimum calculation here matches the expected 16.0.
    """
    protocol = Protocol(n=3, t=2)
    participants = [Participant(id=i, cost=2.0, reward=10.0, collateral=5.0, reliability=1.0) for i in range(3)]
    game = Game(protocol, participants, AdversaryConfig())
    profile = (Strategy.HONEST, Strategy.HONEST, Strategy.HONEST)
    
    thresholds = get_destabilization_thresholds(game, profile, split_rule="equal_split")
    
    # equal_split for coalition of 2:
    # max r_i = 8. B* = 2 * 8 = 16.0
    # equal_split for coalition of 1 (behavioral): B* = 1 * 8 = 8.0
    assert thresholds["b_behavioral_star"] == 8.0
    assert thresholds["b_service_star"] == 16.0
