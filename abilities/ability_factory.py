from data.ability_config import ABILITY_CONFIG
from abilities.behaviors.melee import MeleeBehavior
from abilities.behaviors.ranged import RangedBehavior
from abilities.behaviors.defensive import DefensiveBehavior
from abilities.behaviors.decoy import DecoyBehavior


BEHAVIOR_MAP = {
    "melee":     MeleeBehavior,
    "ranged":    RangedBehavior,
    "defensive": DefensiveBehavior,
    "decoy":     DecoyBehavior,
}


class AbilityFactory:
    @staticmethod
    def build(owner, ability_name):
        config = ABILITY_CONFIG.get(ability_name)

        if config is None:
            print(f"[AbilityFactory] Unknown ability: '{ability_name}'")
            return None

        behavior_key = config.get("behavior")

        if behavior_key is None:
            print(f"[AbilityFactory] No behavior defined for ability '{ability_name}'")
            return None

        behavior_class = BEHAVIOR_MAP.get(behavior_key)

        if behavior_class is None:
            print(f"[AbilityFactory] Unknown behavior: '{behavior_key}' for ability '{ability_name}'")
            return None

        return behavior_class(owner, config)