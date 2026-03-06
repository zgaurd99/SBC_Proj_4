import pygame
from core.physics import circle_overlap, normalize


class Projectile:
    def __init__(self, x, y, dx, dy, config, on_hit, owner):
        self.rect = pygame.Rect(x, y, config["width"], config["height"])
        self.owner = owner
        self.on_hit = on_hit

        self.speed = config["projectile_speed"]
        self.max_distance = config["max_distance"]
        self.core_radius = config["width"] // 2

        nx, ny = normalize(dx, dy)
        self.velocity = pygame.Vector2(nx, ny) * self.speed

        self.distance_travelled = 0.0
        self.alive = True

    def update(self, delta_time, targets):
        if not self.alive:
            return

        dt_seconds = delta_time / 1000

        movement = self.velocity * dt_seconds
        self.rect.x += movement.x
        self.rect.y += movement.y

        self.distance_travelled += movement.length()

        if self.distance_travelled >= self.max_distance:
            self.alive = False
            return

        self._check_collisions(targets)

    def _check_collisions(self, targets):
        for target in targets:
            if target == self.owner or not target.alive:
                continue

            if circle_overlap(
                self.rect.centerx, self.rect.centery, self.core_radius,
                target.rect.centerx, target.rect.centery, target.core_radius
            ):
                self.on_hit(self, target, targets)
                self.alive = False
                return

    def draw(self, screen, camera):
        pygame.draw.circle(
            screen,
            (255, 255, 100),
            camera.apply(self.rect).center,
            self.core_radius
        )