import pygame
import sys

from game.game_state import GameState
from ui.hud import HUD

class GameLoop:
    def __init__(self):
        pygame.init()

        self.WIDTH = 1000
        self.HEIGHT = 700

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption("Survival Prototype")

        self.clock = pygame.time.Clock()

        self.state = GameState(self.WIDTH, self.HEIGHT)

        self.running = True

    # =========================================================
    # RUN
    # =========================================================

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
            self.state.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()