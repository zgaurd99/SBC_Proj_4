import pygame

class HUD:
    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font_small = pygame.font.SysFont("consolas", 16)
        self.font_medium = pygame.font.SysFont("consolas", 22)

    def draw(self, screen, game_state):

        self._draw_health_bar(screen, game_state)
        self._draw_anger_bar(screen, game_state)
        self._draw_enemy_count(screen, game_state)

    def _draw_health_bar(self, screen, game_state):

        player = game_state.player

        max_health = player.get_stat("health")
        current_health = player.current_health

        ratio = max(0, current_health / max_health)

        bar_width = 250
        bar_height = 20

        x = 20
        y = 20

        pygame.draw.rect(screen, (60, 60, 60), (x, y, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            (50, 200, 50),
            (x, y, bar_width * ratio, bar_height)
        )

        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        text = self.font_small.render(
            f"HP: {int(current_health)} / {int(max_health)}",
            True,
            (255, 255, 255)
        )
        screen.blit(text, (x + 5, y + 2))

    def _draw_anger_bar(self, screen, game_state):

        anger = game_state.anger_value
        threshold = game_state.spawn_manager.anger_threshold

        ratio = min(1.0, anger / threshold)

        bar_width = 250
        bar_height = 15

        x = 20
        y = 50

        pygame.draw.rect(screen, (60, 60, 60), (x, y, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (x, y, bar_width * ratio, bar_height)
        )

        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        text = self.font_small.render(
            f"Anger: {int(anger)}",
            True,
            (255, 255, 255)
        )
        screen.blit(text, (x + 5, y - 16))

    def _draw_enemy_count(self, screen, game_state):

        count = len(game_state.spawn_manager.enemies)
        cap = game_state.spawn_manager._current_max_enemies()

        text = self.font_medium.render(
            f"Enemies: {count} / {cap}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (20, 80))