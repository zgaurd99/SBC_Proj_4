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
            self.owner.velocity.update(1, 1)

    def on_state_update(self, state, delta_time):
        if state != "active":
            return
        
        for targets in self.owner.game.get_entities_in_radius(self.owner.rect.center, self.radius):
            if targets == self.owner or targets in self._hit_targets:
                continue

            if circle_overlap(
                self.owner.rect.centerx,
                self.owner.rect.centery,
                self.radius,
                targets.rect.centerx,
                targets.rect.centery,
                targets.core_radius
            ):
                # Apply damage
                targets.take_damage(self.damage)

                # Apply knockback
                dx = targets.rect.centerx - self.owner.rect.centerx
                dy = targets.rect.centery - self.owner.rect.centery

                if dx == 0 and dy == 0:
                    continue

                direction = normalize(dx, dy)
                total = self.owner.rigidity + targets.rigidity
                
                if total == 0:
                    continue

                weight = self.owner.rigidity / total
                force = self.base_force * weight
                
                apply_impulse(
                    targets,
                    direction[0],
                    direction[1],
                    force
                )

                targets.stun_timer = targets.stun_duration

                self._hit_targets.add(targets)