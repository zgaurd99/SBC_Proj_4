import math
import random

from abilities.base_abilities import BaseAbility
from entities.decoy import Decoy


class DecoyBehavior(BaseAbility):
    CONTEXT_NEEDS = ["register_entity"]

    def __init__(self, owner, config):
        super().__init__(owner)

        self.windup_time    = config.get("windup_time",    0.0)
        self.active_time    = config.get("active_time",    0.1)
        self.recovery_time  = config.get("recovery_time",  0.0)
        self.cooldown_time  = config.get("cooldown_time",  8.0)
        self.spawn_radius   = config.get("spawn_radius",   60)
        self.lifetime       = config.get("lifetime",       5.0)
        self.health_percent = config.get("health_percent", 0.3)
        self.screen_height  = config.get("screen_height",  270)

        self.register_entity = None
        self._spawned = False

    def on_state_enter(self, state):
        if state == "windup":
            self._spawned = False

    def on_update(self, delta_time, targets=None):
        if not self.is_active() or self._spawned:
            return

        angle = random.uniform(0, 2 * math.pi)
        x = self.owner.rect.centerx + math.cos(angle) * self.spawn_radius
        y = self.owner.rect.centery + math.sin(angle) * self.spawn_radius

        size = int(self.screen_height * 0.05)

        decoy = Decoy(
            int(x), int(y),
            owner=self.owner,
            size=size,
            health_percent=self.health_percent,
            lifetime=self.lifetime
        )

        if self.register_entity:
            self.register_entity(decoy, role="decoy_target")

        self._spawned = True