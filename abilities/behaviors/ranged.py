from abilities.base_abilities import BaseAbility
from core.physics import normalize


class RangedBehavior(BaseAbility):
    def __init__(self, owner, config):
        super().__init__(owner)

        self.windup_time = config["windup_time"]
        self.active_time = config["active_time"]
        self.recovery_time = config["recovery_time"]
        self.cooldown_time = config["cooldown_time"]

        self.projectile_speed = config["projectile_speed"]
        self.damage = config["damage"]
        self.base_force = config["base_force"]
        self.lock_movement = config["lock_movement"]

        self._fired = False

    def on_state_enter(self, state):
        if state == "windup":
            self._fired = False

        if state in ("active", "recovery", "idle"):
            if self.lock_movement:
                self.owner.velocity.update(0, 0)

    def on_update(self, delta_time, targets=None):
        if not self.is_active() or self._fired:
            return

        # TODO: wire into projectile system when implemented
        self._fired = True