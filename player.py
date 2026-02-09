import pygame
import math

class Player:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.health = 100

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

        length = math.sqrt(dx*dx + dy*dy)
        if length != 0:
            dx /= length
            dy /= length

        self.x += dx * self.speed
        self.y += dy * self.speed

        if self.x < 0:
            self.x = 0
        if self.x > width - self.size:
            self.x = width - self.size
        if self.y < 0:
            self.y = 0
        if self.y > height - self.size:
            self.y = height - self.size

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.x, self.y, self.size, self.size)
        )
