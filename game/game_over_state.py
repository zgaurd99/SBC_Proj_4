import pygame
from ui.button import UIButton


class GameOverState:
    def __init__(self, screen_width, screen_height, assets, time_survived, enemies_killed, on_restart):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.assets = assets
        self.on_restart = on_restart

        self.title_font = pygame.font.Font(
            "assets/fonts/04B_30__.TTF",
            max(8, int(screen_height * 0.1))
        )
        self.stat_font = pygame.font.Font(
            "assets/fonts/04B_30__.TTF",
            max(8, int(screen_height * 0.05))
        )

        minutes = time_survived // 60
        seconds = time_survived % 60
        self.lines = [
            f"GAME OVER",
            f"TIME  {minutes:02d}:{seconds:02d}",
            f"KILLS  {enemies_killed}",
        ]

        btn_surface = assets.get("btn_green")
        self.restart_button = UIButton(
            x=screen_width // 2 - btn_surface.get_width() // 2,
            y=int(screen_height * 0.7),
            surface=btn_surface,
            label="RESTART",
            font=self.stat_font,
            callback=on_restart
        )

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.restart_button.handle_click(event.pos)

    def update(self, delta_time):
        pass

    def draw(self, screen):
        screen.fill((10, 10, 10))

        title = self.title_font.render(self.lines[0], True, (220, 60, 60))
        screen.blit(title, title.get_rect(centerx=self.screen_width // 2, y=int(self.screen_height * 0.15)))

        for i, line in enumerate(self.lines[1:]):
            text = self.stat_font.render(line, True, (200, 195, 120))
            screen.blit(text, text.get_rect(centerx=self.screen_width // 2, y=int(self.screen_height * (0.35 + i * 0.15))))

        self.restart_button.draw(screen)