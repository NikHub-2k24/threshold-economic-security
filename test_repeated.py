from core.strategies import Strategy
from core.participants import Participant
from core.protocol import Protocol
from core.adversary import AdversaryConfig
from core.game import Game
from models.repeated_game import check_grim_trigger_sustainability

def test_repeated():
    # Make a game where honest is NOT a Nash equilibrium, so they deviate.
    # But punishment profile is (DEFECT, DEFECT, DEFECT) giving U=-5.
    protocol = Protocol(n=3, t=2, detection_probability_defect=1.0)
    # cost=12, reward=10 -> U(H) = -2.
    # Deviation to A -> U(A) = 0. So gain is +2.
    participants = [Participant(id=i, cost=12.0, reward=10.0, collateral=5.0, reliability=1.0) for i in range(3)]
    game = Game(protocol, participants, AdversaryConfig())
    profile = (Strategy.HONEST, Strategy.HONEST, Strategy.HONEST)
    
    # Let punishment profile be (DEFECT, DEFECT, DEFECT). Wait, is that a Nash Eq?
    # If I defect, I get -5. Can I deviate to A? U(A) = 0.
    # So (DEFECT, DEFECT, DEFECT) is NOT Nash!
    # (ABSTAIN, ABSTAIN, ABSTAIN) gives 0. Can I deviate to H?
    # P(success | 1H) = 0. U(H) = 0 - 12 = -12. 
    # So (ABSTAIN, ABSTAIN, ABSTAIN) IS a Nash Equilibrium!
    
    punishment = (Strategy.ABSTAIN, Strategy.ABSTAIN, Strategy.ABSTAIN)
    
    res = check_grim_trigger_sustainability(game, profile, delta=0.9, punishment_profile=punishment)
    print(res)

test_repeated()
