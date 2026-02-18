import pygame
import sys
import random
import math

from enitites import Player, Enemy
from enemy_data import ENEMY_TYPES
from win32api import GetSystemMetrics

# ---------- init ----------
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

world_width = 3000
world_height = 3000

world_left = 0
world_top = 0
world_right = world_width
world_bottom = world_height

screen = pygame.display.set_mode(
    (screen_width, screen_height),
    pygame.SCALED | pygame.DOUBLEBUF,
    vsync=1
)
pygame.display.set_caption("First Game")

# ---------- player ----------
player = Player(
    world_width // 2 - 10,
    world_height // 2 - 10,
    20, 20, 5, 100
)

# ---------- game state ----------
running = True
game_over = False
start_time = pygame.time.get_ticks()

enemies = []

spawn_timer_max = 60
spawn_timer = 0

# ---------- spawn & culling ellipses ----------
spawn_margin = 0
cull_margin = 200

spawn_rx = screen_width // 2 + spawn_margin
spawn_ry = screen_height // 2 + spawn_margin

cull_rx = screen_width // 2 + cull_margin
cull_ry = screen_height // 2 + cull_margin

# ---------- helpers ----------
def spawn_position_ellipse(px, py):
    angle = random.uniform(0, 2 * math.pi)
    x = px + math.cos(angle) * spawn_rx
    y = py + math.sin(angle) * spawn_ry
    return x, y

def inside_ellipse(dx, dy, rx, ry):
    return (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry) <= 1

# ---------- systems ----------
def handle_events(game_over):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return False

    return True

def spawn_system(enemies, player, spawn_timer):
    spawn_timer += 1
    if spawn_timer >= spawn_timer_max:
        spawn_timer = 0

        x, y = spawn_position_ellipse(
            player.rect.centerx,
            player.rect.centery
        )

        enemies.append(Enemy(x, y, ENEMY_TYPES["basic"]))

    return spawn_timer

def enemy_update_system(enemies, player):
    active = []

    for enemy in enemies:
        dx = enemy.rect.centerx - player.rect.centerx
        dy = enemy.rect.centery - player.rect.centery

        if inside_ellipse(dx, dy, cull_rx, cull_ry):
            enemy.update(player.rect)
            active.append(enemy)

    return active

def separation_system(enemies):
    for i, enemy in enumerate(enemies):
        for other in enemies[i + 1:]:
            dx = enemy.rect.centerx - other.rect.centerx
            dy = enemy.rect.centery - other.rect.centery

            if abs(dx) > 80 or abs(dy) > 80:
                continue

            dist_sq = dx * dx + dy * dy
            min_dist = enemy.core_radius + other.core_radius

            if dist_sq < min_dist * min_dist and dist_sq != 0:
                dist = math.sqrt(dist_sq)
                overlap = min_dist - dist

                push_x = dx / dist * (overlap / 2)
                push_y = dy / dist * (overlap / 2)

                enemy.rect.x += push_x
                enemy.rect.y += push_y
                other.rect.x -= push_x
                other.rect.y -= push_y

def player_enemy_collision_system(player, enemies):
    for enemy in enemies:

        dx = player.rect.centerx - enemy.rect.centerx
        dy = player.rect.centery - enemy.rect.centery

        dist_sq = dx * dx + dy * dy
        min_dist = player.core_radius + enemy.core_radius

        if dist_sq == 0 or dist_sq >= min_dist * min_dist:
            continue

        dist = math.sqrt(dist_sq)
        overlap = min_dist - dist

        nx = dx / dist
        ny = dy / dist

        # balanced separation
        player.rect.x += nx * overlap * 0.4
        player.rect.y += ny * overlap * 0.4

        enemy.rect.x -= nx * overlap * 0.6
        enemy.rect.y -= ny * overlap * 0.6

def damage_system(player, enemies):
    current_time = pygame.time.get_ticks()

    for enemy in enemies:

        dx = enemy.rect.centerx - player.rect.centerx
        dy = enemy.rect.centery - player.rect.centery

        dist_sq = dx * dx + dy * dy
        min_dist = player.core_radius + enemy.core_radius

        # radial collision check
        if dist_sq >= min_dist * min_dist:
            continue

        # player invulnerability check
        if current_time < player.invulnerable_until:
            continue

        # enemy cooldown check
        if current_time - enemy.last_hit_time < enemy.hit_cooldown:
            continue

        # apply damage
        player.take_damage(1)
        player.invulnerable_until = current_time + player.invulnerability_duration
        enemy.last_hit_time = current_time

        if dist_sq == 0:
            continue

        dist = math.sqrt(dist_sq)
        nx = dx / dist
        ny = dy / dist

        # ---- impulse knockback ----
        knockback_strength = 30  # increase for stronger push

        # push player backward
        player.vel_x -= nx * knockback_strength
        player.vel_y -= ny * knockback_strength

        # push enemy backward slightly
        enemy.vel_x += nx * (knockback_strength * 0.5)
        enemy.vel_y += ny * (knockback_strength * 0.5)

        # stun enemy
        enemy.stun_end_time = current_time + enemy.stun_duration



def draw_game(screen, enemies, player, camera_x, camera_y):
    screen.fill((0, 0, 0))

    for enemy in enemies:
        dx = enemy.rect.centerx - player.rect.centerx
        dy = enemy.rect.centery - player.rect.centery

        if inside_ellipse(dx, dy, spawn_rx, spawn_ry):
            enemy.draw(screen, camera_x, camera_y)

    player.draw(screen, camera_x, camera_y)

    # ui
    health_color = (0, 255, 0) if player.health > 5 else (255, 0, 0)
    health_text = font.render(f"Health: {player.health}", True, health_color)
    screen.blit(health_text, (10, 10))

    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(f"Time: {elapsed}s", True, (255, 255, 255))
    screen.blit(time_text, (screen_width - 120, 10))

# ---------- main loop ----------
while running:
    running = handle_events(game_over)

    camera_x = player.rect.centerx - screen_width // 2
    camera_y = player.rect.centery - screen_height // 2

    if not game_over:
        keys = pygame.key.get_pressed()
        player.update(keys)

        spawn_timer = spawn_system(enemies, player, spawn_timer)
        enemies = enemy_update_system(enemies, player)
        
        damage_system(player, enemies)
        player_enemy_collision_system(player, enemies)
        separation_system(enemies)

        if not player.alive:
            game_over = True

    draw_game(screen, enemies, player, camera_x, camera_y)

    if game_over:
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text = font.render("GAME OVER", True, (255, 255, 255))
        hint = font.render("Press ENTER to exit", True, (200, 200, 200))

        screen.blit(
            text,
            (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 30)
        )
        screen.blit(
            hint,
            (screen_width // 2 - hint.get_width() // 2, screen_height // 2 + 10)
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
