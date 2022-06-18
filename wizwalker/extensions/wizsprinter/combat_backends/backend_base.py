from typing import *

from ..combat_config_parser import PriorityLine

class BaseCombatBackend:
    def __init__(self, cast_time: float = 0.2):
        self.cast_time = cast_time
        self.combat = None

    def attach_combat(self, combat): # TODO: Import+type hint not working because of circular import
        self.combat = combat

    def get_real_round(self, r: int) -> Optional[PriorityLine]:
        raise NotImplementedError()

    def get_relative_round(self, r: int) -> Optional[PriorityLine]:
        raise NotImplementedError()
