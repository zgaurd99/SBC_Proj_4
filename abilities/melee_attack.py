from abilities.base_abilities import BaseAbility
from core.physics import circle_overlap, normalize, apply_impulse

class MeleeAttack(BaseAbility):
    def __init__(self, owner):
        super().__init__(owner)
        self.windup_time = 0.25   # short delay before the swing becomes active
        self.active_time = 0.1    # how long the hitbox is live during the swing
        self.recovery_time = 0.25 # time after the swing before the entity can act again
        self.cooldown_time = 0.2  # waiting time before the attack can be used again
        self.radius = 60          # how far the melee attack reaches from the owner's center
        self.damage = 3           # base damage dealt to targets hit
        self.base_force = 35      # base knockback force applied to hit targets
        self.lock_movement = True # whether the player can move during the attack
        self._hit_targets = set() # tracks which targets have already been hit this active phase, prevents double hits

    def on_state_enter(self, state):
        # called whenever the attack transitions into a new phase
        if state == "windup":
            # clear hit targets at the start of each new swing so previous hits don't carry over
            self._hit_targets.clear()

        if state in ("active", "recovery"):
            # freeze the owner's movement during the swing and recovery if movement is locked
            if self.lock_movement:
                self.owner.velocity.update(0, 0)

        if state == "idle":
            # ensure the owner is fully stopped once the ability finishes
            if self.lock_movement:
                self.owner.velocity.update(0, 0)

    def on_update(self, delta_time):
        # only run hit detection during the active phase, skip all other phases
        if not self.is_active():
            return

        # check all nearby entities within the attack radius each frame
        for target in self.owner.game.get_entities_in_radius(
            self.owner.rect.center,
            self.radius
        ):
            # skip the owner itself and any target already hit this swing
            if target == self.owner or target in self._hit_targets:
                continue

            # do a precise circle overlap check between the attack radius and the target's core radius
            if circle_overlap(
                self.owner.rect.centerx,
                self.owner.rect.centery,
                self.radius,
                target.rect.centerx,
                target.rect.centery,
                target.core_radius
            ):
                # apply damage using the dealer system so damage source is tracked
                target.take_damage(self.owner)

                # calculate knockback direction from owner to target
                dx = target.rect.centerx - self.owner.rect.centerx
                dy = target.rect.centery - self.owner.rect.centery
                if dx == 0 and dy == 0:
                    continue  # skip if target is exactly on top of owner, direction undefined

                direction = normalize(dx, dy)

                # scale knockback force based on the ratio of owner rigidity to combined rigidity
                # higher owner rigidity means more force transferred to the target
                owner_rigidity = self.owner.get_stat("rigidity")
                target_rigidity = target.get_stat("rigidity")
                total = owner_rigidity + target_rigidity
                if total == 0:
                    continue  # avoid division by zero if both rigidities are zero

                weight = owner_rigidity / total
                force = self.base_force * weight

                apply_impulse(
                    target,
                    direction[0],
                    direction[1],
                    force
                )

                # calculate stun duration, capped at 1, based on target's stun factor and owner's stun strength
                stun = min(
                    1,
                    target.get_stat("stun_factor") *
                    self.owner.get_stat("stun_strength")
                )
                target.stun_timer = stun

                # mark target as hit so it won't be hit again this swing
                self._hit_targets.add(target)