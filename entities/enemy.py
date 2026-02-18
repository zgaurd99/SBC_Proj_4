import pygame

from entity import Entity

class Enemy(Entity):
    def __init__(self, x, y, config):
        super().__init__(
            x, y,
            config["width"],
            config["height"],
            config["speed"],
            config["health"],
            config["defense"],
            config["rigidity"]
        )
        self.hit_cooldown = config["hit_cooldown"]
        self.last_hit_time = -self.hit_cooldown
        self.gauage_cost = config["gauge_cost"]
        self.colour = config["colour"]
        self.damage = config["damage"]

        self.stun_end_time = 0
        self.stun_duration = 150
    
    def update(self, target_rect):
        current_time = pygame.time.get_ticks()

        if current_time < self.stun_end_time:
            return

        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        self.move(dx, dy)
 
    def draw(self, screen, camera_x, camera_y):
        super().draw(screen, camera_x, camera_y, self.colour)