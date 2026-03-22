import pygame
import sys
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)
user32 = ctypes.windll.user32

from game.game_state import GameState
from game.menu_state import MenuState
from core.asset_loader import AssetLoader
from data.ui_config import UI_MANIFEST
from game.game_over_state import GameOverState

RESOLUTIONS = [
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (3840, 2160),
]

def _pick_resolution(monitor_w, monitor_h):
    fitting = [
        (w, h) for w, h in RESOLUTIONS
        if w <= monitor_w and h <= monitor_h
    ]
    if not fitting:
        return RESOLUTIONS[0]
    return max(fitting, key=lambda r: r[0] * r[1])


class GameLoop:
    def __init__(self):
        pygame.init()

        self.monitor_w = user32.GetSystemMetrics(0)
        self.monitor_h = user32.GetSystemMetrics(1)

        self.screen_w, self.screen_h = _pick_resolution(self.monitor_w, self.monitor_h)

        self.screen = pygame.display.set_mode(
            (self.monitor_w, self.monitor_h),
            pygame.NOFRAME
        )

        self.virtual_surface = pygame.Surface((self.screen_w, self.screen_h))

        self.offset_x = (self.monitor_w - self.screen_w) // 2
        self.offset_y = (self.monitor_h - self.screen_h) // 2

        pygame.display.set_caption("Survival Prototype")
        self.clock = pygame.time.Clock()

        self.assets = AssetLoader(UI_MANIFEST)
        self.running = True

        self._to_menu()

    def _start_game(self):
        self.current_state = GameState(
            self.screen_w,
            self.screen_h,
            self.assets,
            on_game_over=self._game_over
        )

    def _game_over(self, time_survived, enemies_killed):
        self.current_state = GameOverState(
            self.screen_w,
            self.screen_h,
            self.assets,
            time_survived,
            enemies_killed,
            on_restart=self._to_menu
        )

    def _to_menu(self):
        self.current_state = MenuState(
            self.screen_w,
            self.screen_h,
            self.assets,
            on_play=self._start_game,
            offset_x=self.offset_x,
            offset_y=self.offset_y,
            int_scale=1
        )

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.current_state.handle_input(event)
                    if event.button == 3:
                        self.current_state.handle_input(event)

            self.current_state.update(delta_time)
            self.current_state.draw(self.virtual_surface)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.virtual_surface, (self.offset_x, self.offset_y))
            pygame.display.flip()

        pygame.quit()
        sys.exit()