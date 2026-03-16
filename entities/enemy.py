import pygame
from entities.entity import Entity


class Enemy(Entity):
    def __init__(self, x, y, config):
        super().__init__(x, y, config)

        self.gauge_cost = config["gauge_cost"]
        self.colour = config["colour"]
        self.anger_value = config["gauge_cost"]
        self.type_key = None
        self.enemy_id: str| None = None
        sprite_config = config.get("sprite")
        if sprite_config:
            sheet = pygame.image.load(sprite_config["sheet"]).convert_alpha()
            self.sprite = sheet.subsurface(pygame.Rect(
                sprite_config["x"], sprite_config["y"],
                sprite_config["w"], sprite_config["h"]
            ))
        else:
            self.sprite = None

    def update(self, target_rect, delta_time):
        if self.hit_timer > 0:
            self.hit_timer -= delta_time

        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            return

        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        self.move(dx, dy)

    def draw(self, screen, camera, color=None):
        if color is None:
            color = self.colour
        super().draw(screen, camera, color)