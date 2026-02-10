import pygame
import sys
import random

from enitites import Player, Enemy

# initailizes window elements
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")

# initalize player
player = Player(
    width // 2 - 20,
    height // 2 - 20,
    20, 20, 5, 100
)

start_time = pygame.time.get_ticks()

# damage prevention window
damage_cooldown = 1000
last_hit_time = 0

#enemy spawn and store logic
enemies = []
spawn_timer = 0
spawn_delay = 60

# camera co-ordinates
camera_x = 0
camera_y = 0

# running logic
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera_x = player.rect.centerx - width // 2
    camera_y = player.rect.centery - height // 2

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

    # player movement updation
    player_center_x = player.x + player.size // 2
    player_center_y = player.y + player.size // 2

    # moving enemies towards player
    for enemy in enemies:
        enemy.update(player_center_x, player_center_y)

    player_rect = pygame.Rect(player.x, player.y, player.size, player.size)

    current_time = pygame.time.get_ticks()

    # damage calculation logic
    if player.health > 0:
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)

            if player_rect.colliderect(enemy_rect):
                if current_time - last_hit_time >= damage_cooldown:
                    player.health -= 1
                    player.health = max(player.health, 0)
                    last_hit_time = current_time


    # gameover detection
    if player.health <= 0:
        print("Game Over")
        running = False

    screen.fill((0, 0, 0))

    for enemy in enemies:
        enemy.draw(screen)


    player.draw(screen)

    # heath bar colour
    if player.health >= 50:
        health_colour = (0, 255, 33)
    elif player.health >= 20:
        health_colour = (255, 248, 58)
    else:
        health_colour = (255, 0, 0)
    health_text = font.render(f"Health: {player.health}", True, health_colour)

    elapsed_time = (current_time - start_time) // 1000

    minutes = elapsed_time // 60
    seconds = elapsed_time % 60

    time_text = font.render(f"Time : {minutes:02d}:{seconds:02d}",
                            True,
                            (255, 255, 255))

    screen.blit(health_text, (10, 10))
    screen.blit(time_text, (width - 150, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
