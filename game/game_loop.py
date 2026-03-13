import pygame
import sys
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)
user32 = ctypes.windll.user32

from game.game_state import GameState

VIRTUAL_W = 480
VIRTUAL_H = 270


class GameLoop:
    def __init__(self):
        pygame.init()

        self.monitor_w = user32.GetSystemMetrics(0)
        self.monitor_h = user32.GetSystemMetrics(1)

        self.virtual_w = VIRTUAL_W
        self.virtual_h = VIRTUAL_H

        scale_x = self.monitor_w // VIRTUAL_W
        scale_y = self.monitor_h // VIRTUAL_H
        self.int_scale = min(scale_x, scale_y)

        self.game_w = VIRTUAL_W * self.int_scale
        self.game_h = VIRTUAL_H * self.int_scale

        self.offset_x = (self.monitor_w - self.game_w) // 2
        self.offset_y = (self.monitor_h - self.game_h) // 2

        self.screen = pygame.display.set_mode(
            (self.monitor_w, self.monitor_h),
            pygame.NOFRAME
        )

        self.virtual_surface = pygame.Surface((self.virtual_w, self.virtual_h))

        pygame.display.set_caption("Survival Prototype")
        self.clock = pygame.time.Clock()

        self.state = GameState(self.virtual_w, self.virtual_h)
        self.running = True

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.state.handle_input(event)
                    if event.button == 3:
                        self.state.handle_input(event)

            self.state.update(delta_time)
            self.state.draw(self.virtual_surface)

            self.screen.fill((0, 0, 0))

            scaled = pygame.transform.scale(
                self.virtual_surface,
                (self.game_w, self.game_h)
            )
            self.screen.blit(scaled, (self.offset_x, self.offset_y))
            pygame.display.flip()

        pygame.quit()
        sys.exit()