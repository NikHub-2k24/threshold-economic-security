from dataclasses import dataclass
from typing import List, Tuple
from .strategies import Strategy
from .participants import Participant
from .protocol import Protocol
from .adversary import AdversaryConfig
from .incentives import probability_service_succeeds, utility

class Game:
    def __init__(self, protocol: Protocol, participants: List[Participant], adversary: AdversaryConfig):
        self.protocol = protocol
        self.participants = participants
        self.adversary = adversary
        
        # Caching
        self._p_success_cache = {}
        self._utility_cache = {}
        
    def get_p_success(self, profile: Tuple[Strategy, ...]) -> float:
        if profile not in self._p_success_cache:
            self._p_success_cache[profile] = probability_service_succeeds(
                self.protocol, self.participants, profile
            )
        return self._p_success_cache[profile]
        
    def get_utility(self, participant_idx: int, profile: Tuple[Strategy, ...]) -> float:
        cache_key = (participant_idx, profile)
        if cache_key not in self._utility_cache:
            p_success = self.get_p_success(profile)
            self._utility_cache[cache_key] = utility(
                participant_idx, self.protocol, self.participants, profile, p_success
            )
        return self._utility_cache[cache_key]

    def get_profile_utilities(self, profile: Tuple[Strategy, ...]) -> List[float]:
        return [self.get_utility(i, profile) for i in range(len(self.participants))]
