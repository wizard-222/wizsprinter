from typing import *
from enum import Enum, auto

from lark import Lark, Transformer


def get_sprinty_grammar():
    return r"""
            ?start: config
            config: line+
            
            line: round_specifier? move_config [(_pipe move_config)*]? _NEWLINE?
            
            move_config: move (_at target)?
            
            move: (move_pass | (spell enchant?))
            move_pass: "pass"
            
            spell: any_spell | words | string
            enchant: _open_bracket (words | string) _close_bracket
            
            target: (target_type | target_multi)
            target_type: target_self | target_boss | target_enemy | target_ally | target_aoe | target_named
            target_self: _spaced{"self"}
            target_boss: _spaced{"boss"}
            target_enemy: _spaced{"enemy"} (_open_paren INT _close_paren)?
            target_ally: _spaced{"ally"} (_open_paren INT _close_paren)?
            target_aoe: _spaced{"aoe"}
            target_named: words | string
            target_multi: _open_paren target_type [(_comma target_type)*]? _close_paren | target_type [(_comma target_type)*]?
            
            round_specifier: _newlines? "{" expression "}" _newlines?
            
            
            any_spell: _spaced{"any"} _less_than spell_type (_and spell_type)* _greater_than
            spell_type: spell_damage | spell_aoe | spell_heal_self | spell_heal_other | spell_heal | spell_blade | spell_shield | spell_trap | spell_enchant
            spell_damage: _spaced{"damage"}
            spell_aoe: _spaced{"aoe"}
            spell_heal: _spaced{"heal"}
            spell_heal_self: spell_heal _spaced{"self"}
            spell_heal_other: spell_heal _spaced{"other"}
            spell_blade: _spaced{"blade"}
            spell_shield: _spaced{"shield"}
            spell_trap: _spaced{"trap"}
            spell_enchant: _spaced{"enchant"}
            
            expression: INT
            
            words: _newlines? word [word*] _newlines?
            word: NAME | ("0".."9")
            string: _newlines? ESCAPED_STRING _newlines?
            
            
            _open_paren: _spaced{"("}
            _close_paren: _spaced{")"}
            _open_bracket: _spaced{"["}
            _close_bracket: _spaced{"]"}
            _less_than: _spaced{"<"}
            _greater_than: _spaced{">"}
            _comma: _spaced{","}
            
            _at: _spaced{"@"}
            _pipe: _spaced{"|"}
            _and: _spaced{"&"}
            CR: "\r"
            LF: "\n"
            _NEWLINE: CR? LF
            _newlines: [_NEWLINE]*
            
            _spaced{tok}: _newlines? tok _newlines?
            
            
            %import common.INT
            %import common.CNAME -> NAME
            %import common.WS_INLINE
            %import common.ESCAPED_STRING
            
            
            %ignore WS_INLINE
        """


class TargetType(Enum):
    type_self = auto()
    type_boss = auto()
    type_enemy = auto()
    type_ally = auto()
    type_aoe = auto()
    type_named = auto()


class SpellType(Enum):
    type_damage = auto()
    type_aoe = auto()
    type_heal = auto()
    type_heal_self = auto()
    type_heal_other = auto()
    type_blade = auto()
    type_shield = auto()
    type_trap = auto()
    type_enchant = auto()


class Spell:
    pass


class NamedSpell(Spell):
    def __init__(self, name: str, is_literal: bool = False):
        self.name = name
        self.is_literal = is_literal

    def __repr__(self) -> str:
        return f"NamedSpell(name=\"{self.name}\", is_literal={self.is_literal})"


class TemplateSpell(Spell):
    def __init__(self, requirements: List[SpellType]) -> None:
        self.requirements = requirements

    def __repr__(self) -> str:
        return f"TemplateSpell(requirements={self.requirements})"


class Move:
    def __init__(self, card: Spell, enchant: Spell = None):
        self.card = card
        self.enchant = enchant

    def __repr__(self) -> str:
        return f"Move(card={self.card}, enchant={self.enchant})"


class TargetData:
    def __init__(self, target_type: TargetType, extra_data: Any = None, is_literal: bool = False):
        self.target_type = target_type
        self.extra_data = extra_data
        self.is_literal = is_literal

    def __repr__(self) -> str:
        return f"TargetData(target_type={self.target_type}, extra_data={self.extra_data}, is_literal={self.is_literal})"


class MoveConfig:
    def __init__(self, move: Move, target: TargetData = None):
        self.move = move
        self.target = target

    def __repr__(self) -> str:
        return f"MoveConfig(move={self.move}, target={self.target})"


class PriorityLine:
    def __init__(self, priorities: List[MoveConfig], _round: int = None):
        self.priorities = priorities
        self.round = _round

    def __repr__(self) -> str:
        return f"PriorityLine(priorities={self.priorities}, round={self.round})"


class CombatConfig:
    def __init__(self, rounds: List[PriorityLine]):
        self.specific_rounds: dict[int, PriorityLine] = {}
        self.infinite_rounds: list[PriorityLine] = []
        for _round in rounds:
            if _round.round is None:
                self.infinite_rounds.append(_round)
            else:
                self.specific_rounds[_round.round] = _round

    def __repr__(self) -> str:
        return f"CombatConfig(specific_rounds={self.specific_rounds}, infinite_rounds={self.infinite_rounds})"


class TreeToConfig(Transformer):
    def spell(self, items):
        if type(items[0]) is not str:
            return TemplateSpell(items[0])
        else:
            name: str = items[0]
            if name.startswith("\""):
                return NamedSpell(name[1:-1], True)
            return NamedSpell(name, False)

    def enchant(self, items):
        return self.spell(items)

    def move_pass(self, items):
        return NamedSpell("pass")

    def move(self, items):
        return Move(*items)

    def move_config(self, items):
        if len(items) > 1 and type(items[1]) is not TargetType:
            t, n = items[1]
            if type(n) is str and n.startswith("\""):
                return MoveConfig(items[0], TargetData(t, n[1:-1], is_literal=True))
            return MoveConfig(items[0], TargetData(t, n))
        elif len(items) > 1:
            return MoveConfig(items[0], TargetData(items[1]))
        return MoveConfig(items[0])

    def line(self, items):
        if type(items[0]) is int:
            return PriorityLine(items[1:], items[0])
        return PriorityLine(items)

    def config(self, items):
        return CombatConfig(items)

    def target_self(self, _):
        return TargetType.type_self

    def target_boss(self, _):
        return TargetType.type_boss

    def target_enemy(self, items):
        if len(items) > 0:
            return TargetType.type_enemy, items[0]
        return TargetType.type_enemy

    def target_ally(self, items):
        if len(items) > 0:
            return TargetType.type_ally, items[0]
        return TargetType.type_ally

    def target_aoe(self, _):
        return TargetType.type_aoe

    def target_named(self, items):
        return TargetType.type_named, items[0]

    def target_type(self, items):
        return items[0]

    def target(self, items):
        return items[0]

    def any_spell(self, items):
        return items

    def spell_type(self, items):
        return items[0]

    def spell_damage(self, _):
        return SpellType.type_damage

    def spell_aoe(self, _):
        return SpellType.type_aoe

    def spell_heal_self(self, _):
        return SpellType.type_heal_self

    def spell_heal_other(self, _):
        return SpellType.type_heal_other

    def spell_heal(self, _):
        return SpellType.type_heal

    def spell_blade(self, _):
        return SpellType.type_blade

    def spell_shield(self, _):
        return SpellType.type_shield

    def spell_trap(self, _):
        return SpellType.type_trap

    def spell_enchant(self, _):
        return SpellType.type_enchant

    def expression(self, items):
        return items[0]

    def round_specifier(self, items):
        return items[0]

    INT = int

    def word(self, s):
        s, = s
        return s

    def words(self, items) -> str:
        res = ""
        for i in items:
            res += f" {i}"
        return res[1:]

    def string(self, items) -> str:
        res: str = items[0]
        res = res.encode("latin1").decode("unicode_escape")
        return res


class CombatConfigProvider:
    def __init__(self, path: str, cast_time: float = 0.2):
        self.cast_time = cast_time
        self.filename = path
        with open(path) as file:
            self.config: CombatConfig = self.parse_config(file.read())

    def parse_config(self, file_contents) -> CombatConfig:
        grammar = get_sprinty_grammar()

        parser = Lark(grammar)
        tree = parser.parse(file_contents)
        return TreeToConfig().transform(tree)

    def get_real_round(self, r: int) -> Optional[PriorityLine]:
        if r in self.config.specific_rounds:
            return self.config.specific_rounds[r]
        return None

    def get_relative_round(self, r: int) -> PriorityLine:
        # TODO: % 0 is bad. Fix that
        return self.config.infinite_rounds[r % len(self.config.infinite_rounds)]
