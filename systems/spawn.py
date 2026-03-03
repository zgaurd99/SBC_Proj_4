import random
import math

from entities.enemy import Enemy
from data.enemy_data import ENEMY_TYPES


class SpawnManager:
    def __init__(self, world_bounds, spawn_band=200):
        self.world_bounds = world_bounds
        self.spawn_band = spawn_band

        self.spawn_gauge = 0
        self.max_gauge = 10

        # Reduced base rate (tuned for playability)
        self.base_rate = 0.003

        # Per-run pacing variance
        self.run_variance = random.uniform(0.9, 1.1)

        # Scaling state
        self.stage = 0
        self.anger = 0
        self.anger_threshold = 100

        self.time_alive = 0.0  # seconds

        self.base_cap = 5              # starting max enemies
        self.cap_growth_rate = 0.2     # enemies per second
        self.max_cap_limit = 200       # absolute safety limit

        self.enemies = []
        self.enabled = True

    def update(self, delta_time):
        """
        delta_time in milliseconds
        """

        if not self.enabled:
            return

        dt_seconds = delta_time / 1000
        self.time_alive += dt_seconds

        self._increase_gauge(delta_time)
        self._try_spawn()

    def _increase_gauge(self, delta_time):

        stage_scaling = 1 + (self.stage * 0.2)

        spawn_gain = (
            self.run_variance
            * delta_time
            * self.base_rate
            * stage_scaling
        )

        self.spawn_gauge += spawn_gain
        self.spawn_gauge = min(self.spawn_gauge, self.max_gauge)

    def _current_max_enemies(self):
        dynamic_cap = self.base_cap + (self.time_alive * self.cap_growth_rate)
        dynamic_cap = min(dynamic_cap, self.max_cap_limit)
        return int(dynamic_cap)

    def _try_spawn(self):

        # Hard cap check
        if len(self.enemies) >= self._current_max_enemies():
            return

        affordable = [
            name for name, data in ENEMY_TYPES.items()
            if data["gauge_cost"] <= self.spawn_gauge
        ]

        if not affordable:
            return

        enemy_type = random.choice(affordable)
        config = ENEMY_TYPES[enemy_type]

        x, y = self._get_spawn_position()

        enemy = Enemy(x, y, config)
        self.enemies.append(enemy)

        self.spawn_gauge -= config["gauge_cost"]

    def _get_spawn_position(self):

        left, top, right, bottom = self.world_bounds

        cx = (left + right) / 2
        cy = (top + bottom) / 2

        outer_a = (right - left) / 2
        outer_b = (bottom - top) / 2

        inner_a = outer_a - self.spawn_band
        inner_b = outer_b - self.spawn_band

        inner_a = max(10, inner_a)
        inner_b = max(10, inner_b)

        theta = random.uniform(0, 2 * math.pi)
        t = random.uniform(0, 1)

        a = inner_a + (outer_a - inner_a) * t
        b = inner_b + (outer_b - inner_b) * t

        x = cx + a * math.cos(theta)
        y = cy + b * math.sin(theta)

        return int(x), int(y)

    def remove_dead(self):
        self.enemies = [e for e in self.enemies if e.alive]

    def clear_all(self):
        self.enemies.clear()

    def set_stage(self, stage):
        self.stage = stage

    def set_anger(self, anger, threshold):
        self.anger = anger
        self.anger_threshold = threshold

    def freeze(self):
        self.enabled = False

    def unfreeze(self):
        self.enabled = True