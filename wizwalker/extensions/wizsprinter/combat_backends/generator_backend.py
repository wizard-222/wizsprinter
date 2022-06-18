from typing import *

from .backend_base import BaseCombatBackend
from ..combat_config_parser import PriorityLine
from ..sprinty_combat import SprintyCombat

class CombatConfigGenerator(BaseCombatBackend):
    def __init__(self, cast_time: float = 0.2):
        super().__init__(cast_time=cast_time)
    
    def get_real_round(self, r: int) -> Optional[PriorityLine]:
        pass

    def get_relative_round(self, r: int) -> Optional[PriorityLine]:
        return self.get_real_round(r) # it's all automatic, so they mean the same thing