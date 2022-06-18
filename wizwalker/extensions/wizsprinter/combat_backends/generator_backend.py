from typing import *

from .backend_base import BaseCombatBackend
from .combat_api import *
from ..sprinty_combat import SprintyCombat

class CombatConfigGenerator(BaseCombatBackend):
    def __init__(self, cast_time: float = 0.2):
        super().__init__(cast_time=cast_time)
        self.combat: SprintyCombat # restore autocomplete
    
    async def get_real_round(self, r: int) -> Optional[PriorityLine]:
        priorities = [
            MoveConfig(
                move=Move(
                    card=TemplateSpell(requirements=[SpellType.type_damage, SpellType.type_aoe]),
                    enchant=TemplateSpell(requirements=[SpellType.type_enchant], optional=True)
                )
            ),

            MoveConfig(
                move=Move(
                    card=TemplateSpell(requirements=[SpellType.type_damage]),
                    enchant=TemplateSpell(requirements=[SpellType.type_enchant], optional=True)
                ),
                target=TargetData(TargetType.type_enemy)
            ),
            
            MoveConfig(move=Move(
                card=NamedSpell("pass")
            ))
        ]

        # TODO: Maybe dedupe?
        return PriorityLine(priorities=priorities)

    async def get_relative_round(self, r: int) -> Optional[PriorityLine]:
        return self.get_real_round(r) # it's all automatic, so they mean the same thing