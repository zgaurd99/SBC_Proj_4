import pygame

from entity import Entity
from core.state_machine import StateMachine

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
        
        self.invuln_timer = 0.0
        self.invulnerability_duration = 0.3

        self.regen_time = config["regen_time"]
        self.regen_timer = 0.0
        self.regen_amt = config["regen_amt"]

        self.attack_machine = StateMachine("idle")

    def update(self, delta_time):
        self.attack_machine.update(delta_time)
        self.passive_heal(delta_time)

    def draw(self, screen, camera, colour):
        screen_rect = camera.apply(self.rect)
        pygame.draw.rect(screen, (255, 255, 255), screen_rect)
    
    def passive_heal(self, delta_time):
        if self.invuln_timer > 0:
            self.invuln_timer -= delta_time
            if self.invuln_timer < 0:
                self.invuln_timer = 0.0
        

        if self.health < self.max_health:
            self.regen_timer += delta_time
            if self.regen_timer >= self.regen_time:
                self.heal(self.regen_amt)
                self.regen_timer = 0.0
