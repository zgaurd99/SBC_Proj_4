import pygame
import math

class Entity:
    def __init__(self, x, y,
                 width, height,
                 speed, health, defense,
                 rigidity,
                 core_radius = None,
                 ):
        
        self.rect = pygame.Rect(x, y, width, height)
        
        self.speed = speed
        self.health = health
        self.defense = defense
        self.max_health = self.health
        self.rigidity = rigidity

        self.initial_stats = [speed, health, defense, rigidity]

        self.buffs = [1.0, 1.0, 1.0, 1.0]

        self.core_radius = min(width, height) // 2 if core_radius is None else core_radius
        
        self.alive = True

        self.height_offset = 0

        self.vel_x = 0
        self.vel_y = 0
        self.knockback_decay = 0.85

    def move(self, dx, dy):
        length = math.hypot(dx, dy)
        if length != 0:
            dx /= length
            dy /= length

        # base movement
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # knockback velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # decay knockback
        self.vel_x *= self.knockback_decay
        self.vel_y *= self.knockback_decay

    def take_damage(self, amount):
        if not self.alive:
            return

        self.health -= amount // (self.defense * self.buffs[2])
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

    def heal(self, amt):
        self.health += amt
        if self.health > self.max_health:
            self.health = self.max_health

    def stat(self, inc_id):
        if inc_id == 0:
            self.speed *= self.initial_stats[0]
        elif inc_id == 1:
            self.max_health *= self.initial_stats[1]
        elif inc_id == 2:
            self.defense *= self.initial_stats[2]
        elif inc_id == 3:
            self.rigidity *= self.initial_stats[3]
