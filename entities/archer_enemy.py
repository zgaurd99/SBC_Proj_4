import pygame
from entities.enemy import Enemy
from entities.projectiles import Projectile


class ArcherEnemy(Enemy):
    def __init__(self, x, y, config):
        super().__init__(x, y, config)

        self.attack_range = config.get("attack_range", 200)
        self.shoot_timer = 0.0

        self._projectile_config = {
            "width":            config.get("projectile_width", 6),
            "height":           config.get("projectile_height", 6),
            "projectile_speed": config.get("projectile_speed", 120),
            "max_distance":     config.get("max_distance", 300),
        }

        self.projectiles = []

        raw = pygame.image.load("assets/enemies/brittle_archer/arrow.png").convert_alpha()
        size = config.get("projectile_width", 6)
        self.arrow_sprite = pygame.transform.scale(raw, (size * 2, size * 2))

    def update(self, target_rect, delta_time):
        dt_seconds = delta_time / 1000

        if self.hit_timer > 0:
            self.hit_timer -= delta_time

        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            return

        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        dist = (dx * dx + dy * dy) ** 0.5

        if dist > self.attack_range:
            self.move(dx, dy)
            self.shoot_timer = 0.0
        else:
            self.shoot_timer -= dt_seconds
            if self.shoot_timer <= 0:
                self._shoot(dx, dy)
                self.shoot_timer = 1.0 / self.get_stat("attack_speed")

    def _shoot(self, dx, dy):
        proj = Projectile(
            self.rect.centerx,
            self.rect.centery,
            dx, dy,
            self._projectile_config,
            on_hit=self._on_projectile_hit,
            owner=self,
            sprite=self.arrow_sprite
        )
        self.projectiles.append(proj)

    def _on_projectile_hit(self, projectile, target, targets):
        target.take_damage(self)