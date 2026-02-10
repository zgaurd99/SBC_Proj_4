import pygame
import math

class Player:
    def __init__(self, x, y, size, speed):
        self.size = size
        self.speed = speed
        self.health = 100
        self.rect = pygame.Rect(x, y, size, size)

    def update(self, keys, width, height):
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

        length = math.hypot(dx, dy)
        if length != 0:
            dx /= length
            dy /= length

        self.x += dx * self.speed
        self.y += dy * self.speed

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