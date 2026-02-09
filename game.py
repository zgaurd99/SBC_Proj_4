import pygame
import sys
import random

from player import Player
from enemy import Enemy

pygame.init()
clock = pygame.time.Clock()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")

player = Player(
    width // 2 - 20,
    height // 2 - 20,
    size=40,
    speed=5
)

enemies = []
spawn_timer = 0
spawn_delay = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        spawn_timer = 0

        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            x = random.randint(0, width)
            y = -30
        elif side == "bottom":
            x = random.randint(0, width)
            y = height + 30
        elif side == "left":
            x = -30
            y = random.randint(0, height)
        else:
            x = width + 30
            y = random.randint(0, height)

        enemies.append(Enemy(x, y))

    keys = pygame.key.get_pressed()
    player.update(keys, width, height)

    player_center_x = player.x + player.size // 2
    player_center_y = player.y + player.size // 2

    for enemy in enemies:
        enemy.update(player_center_x, player_center_y)

    screen.fill((0, 0, 0))

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
