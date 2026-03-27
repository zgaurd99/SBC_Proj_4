import pygame
import random


TREE_W = 60
TREE_H = 80
TREE_ROWS = 3

TILE_SIZE = 32

TILE_PATHS = [
    "assets/world/tile_0000.png",
    "assets/world/tile_0001.png",
    "assets/world/tile_0002.png",
]
TILE_WEIGHTS = [200, 50, 10]


class WorldRenderer:
    def __init__(self, world_size):
        self.world_size = world_size
        self.treeline_depth = TREE_ROWS * TREE_H

        self.tree_sprite = pygame.image.load("assets/world/tree.png").convert_alpha()
        self.tree_sprite = pygame.transform.scale(self.tree_sprite, (TREE_W, TREE_H))

        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(path).convert(),
                (TILE_SIZE, TILE_SIZE)
            )
            for path in TILE_PATHS
        ]

        self.tile_map = self._build_tile_map()
        self.tree_positions = self._build_tree_positions()

    def _build_tile_map(self):
        tile_map = {}
        cols = self.world_size // TILE_SIZE + 1
        rows = self.world_size // TILE_SIZE + 1

        for row in range(rows):
            for col in range(cols):
                tile = random.choices(self.tiles, weights=TILE_WEIGHTS, k=1)[0]
                tile_map[(col, row)] = tile

        return tile_map

    def _build_tree_positions(self):
        positions = []
        size = self.world_size

        cols = size // TREE_W + 1
        rows = size // TREE_H + 1

        for row in range(rows):
            for col in range(cols):
                x = col * TREE_W
                y = row * TREE_H

                in_top    = y < self.treeline_depth
                in_bottom = y >= size - self.treeline_depth
                in_left   = x < self.treeline_depth
                in_right  = x >= size - self.treeline_depth

                if in_top or in_bottom or in_left or in_right:
                    positions.append((x, y))

        return positions

    def draw(self, screen, camera):
        self._draw_ground(screen, camera)
        self._draw_trees(screen, camera)

    def _draw_ground(self, screen, camera):
        start_col = int(camera.x // TILE_SIZE)
        start_row = int(camera.y // TILE_SIZE)
        end_col   = int((camera.x + camera.S_W) // TILE_SIZE) + 1
        end_row   = int((camera.y + camera.S_H) // TILE_SIZE) + 1

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                tile = self.tile_map.get((col, row))
                if tile is None:
                    continue
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                screen_pos = camera.apply(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                screen.blit(tile, screen_pos)

    def _draw_trees(self, screen, camera):
        cam_rect = pygame.Rect(camera.x, camera.y, camera.S_W, camera.S_H)
        for x, y in self.tree_positions:
            tree_rect = pygame.Rect(x, y, TREE_W, TREE_H)
            if cam_rect.colliderect(tree_rect):
                screen.blit(self.tree_sprite, camera.apply(tree_rect))