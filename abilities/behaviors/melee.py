import math
from abilities.base_abilities import BaseAbility
from core.physics import circle_overlap, normalize, apply_impulse


class MeleeBehavior(BaseAbility):
    def __init__(self, owner, config):
        super().__init__(owner)

        self.windup_time    = config["windup_time"]
        self.active_time    = config["active_time"]
        self.recovery_time  = config["recovery_time"]
        self.cooldown_time  = config["cooldown_time"]

        self.radius         = config["radius"]
        self.damage         = config["damage"]
        self.base_force     = config["base_force"]
        self.lock_movement  = config["lock_movement"]
        self.arc_angle      = config.get("arc_angle", 60)

        self.swing_direction  = (1.0, 0.0)
        self._direction_locked = False
        self._hit_targets      = set()

    def on_state_enter(self, state):
        if state == "windup":
            self._hit_targets.clear()
            self._direction_locked = False

        if state == "active":
            self._direction_locked = True

        if state in ("active", "recovery", "idle"):
            if self.lock_movement:
                self.owner.velocity.update(0, 0)

    def on_update(self, delta_time, targets=None, mouse_world_pos=None):
        # Always track mouse until direction is locked
        if not self._direction_locked and mouse_world_pos is not None:
            dx = mouse_world_pos[0] - self.owner.rect.centerx
            dy = mouse_world_pos[1] - self.owner.rect.centery
            nx, ny = normalize(dx, dy)
            if nx != 0 or ny != 0:
                self.swing_direction = (nx, ny)

        if not self.is_active():
            return

        swing_dx, swing_dy = self.swing_direction
        half_angle_rad = math.radians(self.arc_angle)

        for target in (targets or []):
            if target == self.owner or target in self._hit_targets:
                continue

            if not circle_overlap(
                self.owner.rect.centerx, self.owner.rect.centery, self.radius,
                target.rect.centerx,     target.rect.centery,     target.core_radius
            ):
                continue

            tdx = target.rect.centerx - self.owner.rect.centerx
            tdy = target.rect.centery - self.owner.rect.centery
            tnx, tny = normalize(tdx, tdy)

            dot = swing_dx * tnx + swing_dy * tny
            if dot < math.cos(half_angle_rad):
                continue

            target.take_damage(self.owner)

            if tdx == 0 and tdy == 0:
                self._hit_targets.add(target)
                continue

            owner_rigidity  = self.owner.get_stat("rigidity")
            target_rigidity = target.get_stat("rigidity")
            total = owner_rigidity + target_rigidity
            if total == 0:
                self._hit_targets.add(target)
                continue

            weight = owner_rigidity / total
            force  = self.base_force * weight
            apply_impulse(target, tnx, tny, force)

            stun = min(
                1,
                target.get_stat("stun_factor") *
                self.owner.get_stat("stun_strength")
            )
            target.stun_timer = stun
            self._hit_targets.add(target)