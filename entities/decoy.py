from entities.entity import Entity

DECOY_CONFIG = {
    "width":          10,
    "height":         10,
    "defense":        1.0,
    "attack":         0,
    "attack_speed":   1.0,
    "speed":          0,
    "rigidity":       10,
    "stun_factor":    1.0,
    "stun_strength":  1.0,
    "crit_chance":    0.0,
    "crit_multiplier":1.0,
}

class Decoy(Entity):
    def __init__(self, x, y, owner, health_percent=0.3, lifetime=5.0):
        config = DECOY_CONFIG.copy()
        config["health"] = max(1, owner.get_stat("health") * health_percent)

        super().__init__(x, y, config)
        self.lifetime = lifetime
        self.lifetime_timer = 0.0
        self.level = 1

    def update(self, delta_time):
        dt_seconds = delta_time / 1000
        self.lifetime_timer += dt_seconds

        if self.lifetime_timer >= self.lifetime or self.current_health <= 0:
            self.alive = False

    def draw(self, screen, camera, color=(255, 200, 0)):
        super().draw(screen, camera, color)