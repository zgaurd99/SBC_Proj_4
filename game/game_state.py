import pygame

from entities.player import Player
from data.player_data import PLAYER_DATA
from systems.spawn import SpawnManager
from systems.movement import movement_system
from systems.damage import damage_system
from systems.collision import (
    player_enemy_collision_system,
    enemy_enemy_collision_system
)
from core.camera import Camera
from ui.hud import HUD


class GameState:
    def __init__(self, screen_width, screen_height):

        world_size = screen_width * 3  # square world

        self.world_bounds = (0, 0, world_size, world_size)

        self.camera = Camera(
            screen_width,
            screen_height,
            world_size,
            world_size
        )

        # Player placeholder: 5% of virtual height
        player_size = int(screen_height * 0.05)

        player_config = PLAYER_DATA["P1"].copy()
        player_config["width"] = player_size
        player_config["height"] = player_size

        self.player = Player(
            world_size // 2,
            world_size // 2,
            player_config
        )

        self.hud = HUD(screen_width, screen_height)

        self.spawn_manager = SpawnManager(
            self.world_bounds,
            spawn_band=200,
            virtual_h=screen_height
        )

        self.spawn_manager.set_stage(0)
        self.spawn_manager.set_anger(0, 100)

        self.anger_value = 0

    def update(self, delta_time):

        # --- Anger Simulation (temporary) ---
        self.spawn_manager.set_anger(self.anger_value, 100)

        # --- Spawn ---
        self.spawn_manager.update(delta_time, self.player.rect)
        for enemy in self.spawn_manager.enemies[:]:
            if not enemy.alive:
                self._handle_enemy_death(enemy)
                self.spawn_manager.enemies.remove(enemy)

        # --- Input Movement ---
        keys = pygame.key.get_pressed()

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

        movement_system(
            self.player,
            (dx, dy),
            self.world_bounds,
            delta_time
        )

        self.player.update(delta_time, self.spawn_manager.enemies)

        # --- Enemy AI ---
        for enemy in self.spawn_manager.enemies:
            enemy.update(self.player.rect, delta_time)

        # --- Damage ---
        damage_system(
            self.player,
            self.spawn_manager.enemies,
            delta_time
        )

        # --- Collision ---
        player_enemy_collision_system(
            self.player,
            self.spawn_manager.enemies
        )

        enemy_enemy_collision_system(
            self.spawn_manager.enemies
        )

        # --- Camera ---
        self.camera.update(self.player.rect)

    def draw(self, screen):

        screen.fill((20, 20, 20))

        # World border
        world_rect = pygame.Rect(self.world_bounds)
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            self.camera.apply(world_rect),
            2
        )

        # Y sorted drawing for entities
        entities = list(self.spawn_manager.enemies) + [self.player]
        entities.sort(key=lambda e: e.rect.bottom)

        for entity in entities:
            if entity == self.player:
                entity.draw(screen, self.camera, (50, 200, 50))
            else:
                entity.draw(screen, self.camera)

        for ability in self.player.active_abilities:
            if ability.is_active():
                pygame.draw.circle(
                    screen,
                    (255, 255, 0, 128),
                    self.camera.apply(self.player.rect).center,
                    ability.radius,
                    2
                )

        # hud
        self.hud.draw(screen, self)

    def _handle_enemy_death(self, enemy):

        # Increase anger only on kill
        self.anger_value += enemy.anger_value

        threshold = self.spawn_manager.anger_threshold

        if self.anger_value >= threshold:

            # Convert anger overflow into spawn gauge
            overflow = self.anger_value - threshold

            self.spawn_manager.spawn_gauge += threshold * 0.5

            self.anger_value = overflow
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   # left click - slot 0 (sword)
                self.player.trigger_active(0)
            elif event.button == 3: # right click - slot 1 (bow)
                self.player.trigger_active(1)