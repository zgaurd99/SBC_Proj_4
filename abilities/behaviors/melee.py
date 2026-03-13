from abilities.base_abilities import BaseAbility
from core.physics import circle_overlap, normalize, apply_impulse


class MeleeBehavior(BaseAbility):
    def __init__(self, owner, config):
        super().__init__(owner)

        self.windup_time = config["windup_time"]
        self.active_time = config["active_time"]
        self.recovery_time = config["recovery_time"]
        self.cooldown_time = config["cooldown_time"]

        self.radius = config["radius"]
        self.damage = config["damage"]
        self.base_force = config["base_force"]
        self.lock_movement = config["lock_movement"]

        self._hit_targets = set()

    def on_state_enter(self, state):
        if state == "windup":
            self._hit_targets.clear()

        if state in ("active", "recovery", "idle"):
            if self.lock_movement:
                self.owner.velocity.update(0, 0)

    def on_update(self, delta_time, targets=None):
        if not self.is_active():
            return

        for target in (targets or []):
            if target == self.owner or target in self._hit_targets:
                continue

            if not circle_overlap(
                self.owner.rect.centerx,
                self.owner.rect.centery,
                self.radius,
                target.rect.centerx,
                target.rect.centery,
                target.core_radius
            ):
                continue

            target.take_damage(self.owner)

            dx = target.rect.centerx - self.owner.rect.centerx
            dy = target.rect.centery - self.owner.rect.centery

            if dx == 0 and dy == 0:
                continue

            nx, ny = normalize(dx, dy)

            owner_rigidity = self.owner.get_stat("rigidity")
            target_rigidity = target.get_stat("rigidity")

            total = owner_rigidity + target_rigidity
            if total == 0:
                continue

            weight = owner_rigidity / total
            force = self.base_force * weight

            apply_impulse(target, nx, ny, force)

            stun = min(
                1,
                target.get_stat("stun_factor") *
                self.owner.get_stat("stun_strength")
            )
            target.stun_timer = stun

            self._hit_targets.add(target)

            print(f"hit {target} | state: {self.machine.state} | already hit: {target in self._hit_targets}")