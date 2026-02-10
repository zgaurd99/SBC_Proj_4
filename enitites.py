import pygame
import math

class Entity:
    def __init__(self, x, y, width, height, speed, health):
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.alive = True
        self.height_offset = 0

    def move(self, dx, dy):
        length = math.hypot(dx, dy)
        if length != 0:
            dx /= length
            dy /= length

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def take_damage(self, amount):
        if not self.alive:
            return

        self.health -= amount
        if self.health <= 0:
            self.alive = False
            self.on_death()

    def draw(self, screen, camera_x, camera_y, color):
        pygame.draw.rect(
            screen,
            color,
            (
                self.rect.x - camera_x,
                self.rect.y - camera_y,
                self.rect.width,
                self.rect.height
            )
        )

    def on_death(self):
        pass

class Player(Entity):
    def __init__(self, x, y, width, height, speed, health):
        super().__init__(x, y, width, height, speed, health)

    def update(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        self.move(dx, dy)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.rect.x - camera_x,
             self.rect.y - camera_y,
             self.rect.width,
             self.rect.height
            )
        )

class Enemy(Entity):
    def __init__(self, x, y, config):
        super().__init__(
            x, y,
            config["width"],
            config["height"],
            config["speed"],
            config["health"]
        )
        self.hit_cooldown = config["hit_cooldown"]
        self.last_hit_time = 0
        
        self.separation_radius = config["separation_radius"]

        self.gauage_cost = config["gauge_cost"]
    
    def update(self, target_rect):
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        self.move(dx, dy)

    
    def draw(self, screen, camera_x, camera_y):
        super().draw(screen, camera_x, camera_y, (200, 50, 50))