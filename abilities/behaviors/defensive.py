from abilities.base_abilities import BaseAbility


class DefensiveBehavior(BaseAbility):
    def __init__(self, owner, config):
        super().__init__(owner)

        self.windup_time = config.get("windup_time", 0)
        self.active_time = config.get("active_time", 0)
        self.recovery_time = config.get("recovery_time", 0)
        self.cooldown_time = config.get("cooldown_time", 0)

        self.defense_modifier = config.get("defense_modifier", 0.0)
        self.modifier_type = config.get("modifier_type", "percent")

        # TODO: active shield support
        # self.damage_reduction = config.get("damage_reduction", 1.0)
        # self.lock_movement = config.get("lock_movement", False)

    def on_state_enter(self, state):
        pass

    def apply_passive(self):
        """
        Called once when the ability is equipped.
        Adds a permanent stat modifier for the run.
        """
        self.owner.stats.stats["defense"].add_modifier(
            self.defense_modifier,
            self.modifier_type
        )

    def on_update(self, delta_time, targets=None):
        pass