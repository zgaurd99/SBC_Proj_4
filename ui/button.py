import pygame


class UIButton:
    def __init__(self, x, y, surface, label, font, callback):
        self.surface = surface
        self.rect = pygame.Rect(x, y, surface.get_width(), surface.get_height())
        self.label = label
        self.font = font
        self.callback = callback

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

        if not self.label:
            return

        text = self.font.render(self.label, True, (255, 255, 255))

        # Scale text down if it overflows button width
        max_w = int(self.rect.width * 0.75)
        max_h = int(self.rect.height * 0.5)

        if text.get_width() > max_w or text.get_height() > max_h:
            scale = min(max_w / text.get_width(), max_h / text.get_height())
            new_w = max(1, int(text.get_width() * scale))
            new_h = max(1, int(text.get_height() * scale))
            text = pygame.transform.smoothscale(text, (new_w, new_h))

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)