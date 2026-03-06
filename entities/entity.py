import pygame
import math
import random

class Stats:
    def __init__(self,base):
        self.base = base
        self.modifiers = []

    def add_modifier(self, value, mod_type):
        self.modifiers.append((value, mod_type))

    def clear_modifiers(self):
        self.modifiers.clear()

    @property
    def value(self):
        total = self.base
        percent = 0

        for value, mod_type in self.modifiers:
            if mod_type == "flat":
                total += value
            elif mod_type == "percent":
                percent += value

        return total * (1 + percent)

class Entity_Stats_Component:
    def __init__(self, config):
        self.stats = {
            "attack":           Stats(config["attack"]),            # How much damage the entity deals
            "health":           Stats(config["health"]),            # How much damage the entity can take before dying
            "defense":          Stats(config["defense"]),           # How much the entity reduces incoming damage by
            "speed":            Stats(config["speed"]),             # How fast the entity moves
            "rigidity":         Stats(config["rigidity"]),          # How much the entity resists knockback and stun
            "attack_speed":     Stats(config["attack_speed"]),      # How fast the entity attacks (affects attack cooldown)
            "stun_factor":      Stats(config["stun_factor"]),       # How much the entity's stun duration is multiplied by when hit
            "stun_strength":    Stats(config["stun_strength"]),     # How much the entity's stun duration is increased by when hit
            "crit_chance":      Stats(config["crit_chance"]),       # The chance for the entity to deal a critical hit (as a decimal, e.g. 0.25 for 25%)
            "crit_multiplier":  Stats(config["crit_multiplier"])    # How much the entity's damage is multiplied by when it lands a critical hit (e.g. 1.5 for 50% more damage)
        }

class Entity:
    def __init__(self, x, y, config, core_radius=None):
        width = config["width"] if "width" in config else 50
        height = config["height"] if "height" in config else 50
        
        self.rect = pygame.Rect(x, y, width, height)
        
        #stats
        self.stats = Entity_Stats_Component(config)
        self.current_health = self.stats.stats["health"].value

        self.core_radius = min(width, height) // 2 if core_radius is None else core_radius
        
        self.alive = True
        self.height_offset = 0
        self.damage_reduction = 1.0

        self.velocity = pygame.Vector2(0, 0)
        self.knockback_decay = 0.85
        self.stun_timer = 0.0
        self.hit_timer = 0.0
        
    def get_stat(self, name):
        return self.stats.stats[name].value

    @staticmethod
    def chance(percent):
        return random.random() < percent

    def move(self, dx, dy):
        length = math.hypot(dx, dy)
        if length != 0:
            dx /= length
            dy /= length

        # base movement
        speed = self.stats.stats["speed"].value
        self.rect.x += dx * speed
        self.rect.y += dy * speed

        # knockback velocity
        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

        # decay knockback
        self.velocity.x *= self.knockback_decay
        self.velocity.y *= self.knockback_decay

    def take_damage(self, dealer : "Entity"):
        if not self.alive:
            return

        attack = dealer.get_stat("attack")
        crit_chance = dealer.get_stat("crit_chance")
        crit_multiplier = dealer.get_stat("crit_multiplier") if Entity.chance(crit_chance) else 1
        defense = self.get_stat("defense")
        
        final_damage = max(1, (attack/defense) * crit_multiplier)
        self.current_health -= final_damage
        if self.current_health <= 0:
            self.alive = False
            self.on_death()

    def draw(self, screen, camera, color):
        render_rect = self.rect.copy()
        render_rect.y -= self.height_offset

        screen_rect = camera.apply(render_rect)


        pygame.draw.rect(
            screen,
            color,
            screen_rect
        )

    def on_death(self):
        pass

    def heal(self, amt):
        max_health = self.get_stat("health")
        self.current_health = min(self.current_health + amt, max_health)
