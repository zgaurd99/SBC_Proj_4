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
        self.draw_scale = config.get("draw_scale", 0.08)
        self.screen_height = config.get("screen_height", 270)
        self.follow_decoy = config.get("follow_decoy", True)

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

        render_rect = self.rect.copy()
        render_rect.y -= self.height_offset
        screen_rect = camera.apply(render_rect)

        if self.sprite:
            pixel_size = int(self.screen_height * self.draw_scale)
            scaled = pygame.transform.scale(self.sprite, (pixel_size, pixel_size))
            # Centre the sprite on the entity's screen rect
            draw_x = screen_rect.centerx - pixel_size // 2
            draw_y = screen_rect.centery - pixel_size // 2
            screen.blit(scaled, (draw_x, draw_y))
        else:
            pygame.draw.rect(screen, color, screen_rect)