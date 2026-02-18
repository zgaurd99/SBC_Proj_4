import pygame

from entity import Entity

class Player(Entity):
    def __init__(self, x, y, config):
        super().__init__(
            x, y,
            width = config["width"],
            height = config["height"],
            speed = config["speed"] * config["boosts"][0],
            health = config["health"] * config["boosts"][1],
            defense = config["defense"] * config["boosts"][2],
            rigidity = config["rigidity"] * config["boosts"][3]
        )
        
        self.invulnerable_until = 0
        self.invulnerability_duration = 300

        self.regen_time = config["regen_time"]
        self.regen_amt = config["regen_amt"]

    def update(self, keys,):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        self.move(dx, dy)

        self.passive_heal()

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.rect.x - camera_x,
             self.rect.y - camera_y,
             self.rect.width,
             self.rect.height
            )
        )
    
    def passive_heal(self):
        self.regen_time -= 1

        if self.health < self.max_health and self.regen_time == 0:
            self.health += self.regen_amt
