import random
import math
from collections import deque

from entities.enemy import Enemy
from data.enemy_data import ENEMY_TYPES
from entities.archer_enemy import ArcherEnemy

BASE_CAPS = {
    "basic": 6,
    "fast":  4,
    "tank":  2,
    "archer": 3,
}

ENEMY_CLASS_MAP = {
    "archer": ArcherEnemy,
}

MAX_SPAWN_RETRIES = 10
PUSH_INTERVAL     = 5  # ms

class SpawnManager:
    def __init__(self, world_bounds, spawn_band=200, virtual_h=240):
        self.world_bounds  = world_bounds
        self.spawn_band    = spawn_band
        self.virtual_h     = virtual_h

        self.screen_width  = int(virtual_h * (16 / 9))
        self.screen_height = virtual_h

        self.spawn_gauge = 1
        self.max_gauge   = 10

        self.base_rate     = 0.5
        self.run_variance  = random.uniform(0.9, 1.1)

        self.stage = 0
        self.anger = 0
        self.anger_threshold = 100

        self.time_alive = 0.0

        self.enemies = []
        self.queue   = deque()

        self._push_timer = 0.0

        self.enabled = True
        self._id_counter = 0

    def update(self, delta_time, player_rect=None):
        """
        delta_time in milliseconds.
        """
        if not self.enabled:
            return

        dt_seconds = delta_time / 1000
        self.time_alive += dt_seconds

        self._update_max_gauge()
        self._fill_gauge(delta_time)

        self._push_timer += delta_time
        if self._push_timer >= PUSH_INTERVAL:
            self._push_timer = 0.0
            self._try_push()

        self._try_pop(player_rect)

    def _update_max_gauge(self):
        anger = self.anger

        if anger <= 100:
            self.max_gauge = 10 + 15 * math.pow(anger / 100, 0.6)
        elif anger <= 500:
            t = (anger - 100) / 400
            self.max_gauge = 25 + 50 * math.pow(t, 0.7)
        else:
            self.max_gauge = 75 + (anger - 500) * 0.1

    def _fill_gauge(self, delta_time):
        stage_scaling = 1 + (self.stage * 0.2)

        gain = (
            self.run_variance
            * delta_time
            * self.base_rate
            * stage_scaling
        )

        self.spawn_gauge = min(self.spawn_gauge + gain, self.max_gauge)

    def _anger_multiplier(self):
        anger = self.anger

        if anger <= 10:
            return 1.0
        elif anger <= 50:
            t = (anger - 10) / 40
            return 1.0 + t * 1.0
        elif anger <= 200:
            t = (anger - 50) / 150
            return 2.0 + t * 1.0
        else:
            return 3.0 + math.log(1 + (anger - 200) / 200)

    def _type_cap(self, enemy_type):
        base = BASE_CAPS.get(enemy_type, 2)
        return max(1, int(base * self._anger_multiplier()))

    def _queued_count(self, enemy_type):
        return sum(1 for e in self.queue if e == enemy_type)

    def _active_count(self, enemy_type):
        queued  = self._queued_count(enemy_type)
        spawned = sum(
            1 for e in self.enemies
            if e.alive and e.type_key == enemy_type
        )
        return spawned + queued
    
    def _eligible_types(self):
        eligible = []
        for enemy_type in ENEMY_TYPES:
            if self._active_count(enemy_type) < self._type_cap(enemy_type):
                eligible.append(enemy_type)
        return eligible

    def _pick_type(self, eligible):
        weights = [
            self.max_gauge / (ENEMY_TYPES[t]["gauge_cost"] * 3)
            for t in eligible
        ]
        total = sum(weights)
        r = random.uniform(0, total)
        cumulative = 0
        for t, w in zip(eligible, weights):
            cumulative += w
            if r <= cumulative:
                return t
        return eligible[-1]

    def _try_push(self):
        eligible = self._eligible_types()
        if not eligible:
            return

        enemy_type = self._pick_type(eligible)
        self.queue.append(enemy_type)

    def _try_pop(self, player_rect=None):
        if not self.queue:
            return

        enemy_type = self.queue[0]
        config     = ENEMY_TYPES[enemy_type].copy()
        config["screen_height"] = self.virtual_h

        if self.spawn_gauge < config["gauge_cost"]:
            return

        position = self._get_spawn_position(player_rect)
        if position is None:
            return

        x, y = position
        enemy_class = ENEMY_CLASS_MAP.get(enemy_type, Enemy)
        enemy = enemy_class(x, y, config)
        self._id_counter += 1
        enemy.type_key = enemy_type
        enemy.enemy_id = f"{enemy_type}-{hex(self._id_counter)}"
        self.enemies.append(enemy)
        self.spawn_gauge -= config["gauge_cost"]
        self.queue.popleft()

    def _get_spawn_position(self, player_rect=None):
        left, top, right, bottom = self.world_bounds

        if player_rect:
            cx = player_rect.centerx
            cy = player_rect.centery
        else:
            cx = (left + right) / 2
            cy = (top  + bottom) / 2

        rx = self.screen_width  // 2 + self.spawn_band
        ry = self.screen_height // 2 + self.spawn_band

        for _ in range(MAX_SPAWN_RETRIES):
            theta = random.uniform(0, 2 * math.pi)
            x = cx + math.cos(theta) * rx
            y = cy + math.sin(theta) * ry

            if left <= x <= right and top <= y <= bottom:
                return int(x), int(y)

        return None

    def remove_dead(self):
        self.enemies = [e for e in self.enemies if e.alive]

    def clear_all(self):
        self.enemies.clear()
        self.queue.clear()

    def set_stage(self, stage):
        self.stage = stage

    def set_anger(self, anger, threshold):
        self.anger = anger
        self.anger_threshold = threshold

    def freeze(self):
        self.enabled = False

    def unfreeze(self):
        self.enabled = True