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
        self.gauage_cost = config["gauge_cost"]
        self.colour = config["colour"]
        self.damage = config["damage"]

        self.stun_timer = 0.0
        self.stun_duration = 0.15

        self.hit_timer = 0.0
    
    def update(self, target_rect, delta_time):
        if self.hit_timer > 0:
                    self.hit_timer -= delta_time

        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            return
        
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        self.move(dx, dy)
 
    def draw(self, screen, camera):
        super().draw(screen, camera, self.colour)