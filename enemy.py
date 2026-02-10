import pygame
import math

class Enemy:
    def __init__(self, x, y,width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self, target_x, target_y):
        dx = target_x - (self.x + self.size // 2)
        dy = target_y - (self.y + self.size // 2)

        length = math.sqrt(dx*dx + dy*dy)
        if length != 0:
            dx /= length
            dy /= length

        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def draw(self, screen, camera_x):
        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (self.x, self.y, self.size, self.size)
        )
