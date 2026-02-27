from abilities.base_abilities import BaseAbility
from core.physics import circle_overlap, normalize, apply_impulse

class MeleeAttack(BaseAbility):
    def __init__(self, owner):
        super().__init__(owner)

        self.windup_time = 0.25
        self.active_time = 0.1
        self.recovery_time = 0.25
        self.cooldown_time = 0.2

        self.radius = 60
        self.damage = 3
        self.base_force = 35
        
        self.lock_movement = True # Wheter player can move during the attack

        self._hit_targets = set() # To track which targets have already been hit during the active phase

    def on_state_enter(self, state):
        if state == "windup":
            self._hit_targets.clear()

        if state in ("active", "recovery"):
            if self.lock_movement:
                self.owner.velocity.update(0, 0)

        if state == "idle":
            if self.lock_movement:
                self.owner.velocity.update(0, 0)

    def on_update(self, delta_time):
        if not self.is_active():
            return

        for target in self.owner.game.get_entities_in_radius(
            self.owner.rect.center,
            self.radius
        ):
            if target == self.owner or target in self._hit_targets:
                continue

            if circle_overlap(
                self.owner.rect.centerx,
                self.owner.rect.centery,
                self.radius,
                target.rect.centerx,
                target.rect.centery,
                target.core_radius
            ):
                # Apply damage using dealer system
                target.take_damage(self.owner)

                # Knockback
                dx = target.rect.centerx - self.owner.rect.centerx
                dy = target.rect.centery - self.owner.rect.centery

                if dx == 0 and dy == 0:
                    continue

                direction = normalize(dx, dy)

                owner_rigidity = self.owner.get_stat("rigidity")
                target_rigidity = target.get_stat("rigidity")

                total = owner_rigidity + target_rigidity
                if total == 0:
                    continue

                weight = owner_rigidity / total
                force = self.base_force * weight

                apply_impulse(
                    target,
                    direction[0],
                    direction[1],
                    force
                )

                # Stun scaling
                stun = min(
                    1,
                    target.get_stat("stun_factor") *
                    self.owner.get_stat("stun_strength")
                )
                target.stun_timer = stun

                self._hit_targets.add(target)