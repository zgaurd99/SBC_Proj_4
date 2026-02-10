import pygame
import sys
import random
import math

from enitites import Player, Enemy
from enemy_data import ENEMY_TYPES

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game")

player = Player(
    width // 2 - 10,
    height // 2 - 10,
    20, 20, 5, 100
)

running = True
game_over = False
start_time = pygame.time.get_ticks()

enemies = []

SPAWN_TIMER_MAX = 60
spawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False

    camera_x = player.rect.centerx - width // 2
    camera_y = player.rect.centery - height // 2

    if not game_over:
        spawn_timer += 1
        if spawn_timer >= SPAWN_TIMER_MAX:
            spawn_timer = 0

            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = camera_x + random.randint(0, width)
                y = camera_y - 40
            elif side == "bottom":
                x = camera_x + random.randint(0, width)
                y = camera_y + height + 40
            elif side == "left":
                x = camera_x - 40
                y = camera_y + random.randint(0, height)
            else:
                x = camera_x + width + 40
                y = camera_y + random.randint(0, height)

            enemies.append(Enemy(x, y, ENEMY_TYPES["basic"]))

        # --- Player movement ---
        keys = pygame.key.get_pressed()
        player.update(keys)

        # --- Enemy movement ---
        for enemy in enemies:
            enemy.update(player.rect)

        # --- Enemy separation (ONCE per frame) ---
        for i, enemy in enumerate(enemies):
            for other in enemies[i + 1:]:
                dx = enemy.rect.centerx - other.rect.centerx
                dy = enemy.rect.centery - other.rect.centery
                dist = math.hypot(dx, dy)

                min_dist = enemy.separation_radius + other.separation_radius

                if dist == 0:
                    continue

                if dist < min_dist:
                    overlap = min_dist - dist
                    push_x = dx / dist * (overlap / 2)
                    push_y = dy / dist * (overlap / 2)

                    enemy.rect.x += push_x
                    enemy.rect.y += push_y
                    other.rect.x -= push_x
                    other.rect.y -= push_y

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                dx = player.rect.centerx - enemy.rect.centerx
                dy = player.rect.centery - enemy.rect.centery
                dist = math.hypot(dx, dy)

                if dist == 0:
                    continue

                overlap_x = (player.rect.width + enemy.rect.width) / 2 - abs(dx)
                overlap_y = (player.rect.height + enemy.rect.height) / 2 - abs(dy)

                if overlap_x > 0 and overlap_y > 0:
                    if overlap_x < overlap_y:
                        push_x = overlap_x if dx > 0 else -overlap_x
                        player.rect.x += push_x * 0.3
                        enemy.rect.x -= push_x * 0.7
                    else:
                        push_y = overlap_y if dy > 0 else -overlap_y
                        player.rect.y += push_y * 0.3
                        enemy.rect.y -= push_y * 0.7


        # --- Damage (per enemy cooldown) ---
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                if current_time - enemy.last_hit_time >= enemy.hit_cooldown:
                    player.take_damage(1)
                    enemy.last_hit_time = current_time

        # --- Cleanup ---
        enemies = [e for e in enemies if e.alive]

        # --- Game over ---
        if not player.alive:
            game_over = True

    # -------- DRAW --------
    screen.fill((0, 0, 0))

    entities_to_draw = enemies + [player]
    for entity in entities_to_draw:
        entity.draw(screen, camera_x, camera_y)

    # --- UI ---
    health_color = (0, 255, 0) if player.health > 5 else (255, 0, 0)
    health_text = font.render(f"Health: {player.health}", True, health_color)
    screen.blit(health_text, (10, 10))

    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(f"Time: {elapsed}s", True, (255, 255, 255))
    screen.blit(time_text, (width - 120, 10))

    # --- GAME OVER OVERLAY ---
    if game_over:
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text = font.render("GAME OVER", True, (255, 255, 255))
        hint = font.render("Press ENTER to exit", True, (200, 200, 200))

        screen.blit(
            text,
            (width // 2 - text.get_width() // 2, height // 2 - 30)
        )
        screen.blit(
            hint,
            (width // 2 - hint.get_width() // 2, height // 2 + 10)
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()