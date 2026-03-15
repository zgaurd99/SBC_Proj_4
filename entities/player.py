import pygame

from entities.entity import Entity
from abilities.ability_factory import AbilityFactory

class Player(Entity):
    def __init__(self, x, y, config):
        super().__init__(x, y, config)

        self.invuln_timer = 0.0
        self.invulnerability_duration = 0.3

        self.regen_time = config["regen_time"]
        self.regen_timer = 0.0
        self.regen_amt = config["regen_amt"]

        self.active_abilities = []
        self.passive_abilities = []

        self._build_abilities(config.get("abilities", {}))

        self.bindings = config.get("abilities", {}).get("bindings", {})

    def _build_abilities(self, abilities_config):
        for ability_name in abilities_config.get("active", []):
            ability = AbilityFactory.build(self, ability_name)
            if ability:
                self.active_abilities.append(ability)

        for ability_name in abilities_config.get("passive", []):
            ability = AbilityFactory.build(self, ability_name)
            if ability:
                self.passive_abilities.append(ability)
                if hasattr(ability, "apply_passive"):
                    ability.apply_passive()

    def equip_passive(self, ability_name):
        """
        Called during a run when the player earns a new passive ability.
        """
        ability = AbilityFactory.build(self, ability_name)
        if ability:
            self.passive_abilities.append(ability)
            if hasattr(ability, "apply_passive"):
                ability.apply_passive()

    def trigger_active(self, index):
        """
        Called by game_state when a keybind is pressed.
        index corresponds to the active ability slot.
        """
        if index < len(self.active_abilities):
            self.active_abilities[index].try_activate()

    def update(self, delta_time, targets=None):
        dt_seconds = delta_time / 1000

        for ability in self.active_abilities:
            ability.update(dt_seconds, targets or [])

        for ability in self.passive_abilities:
            ability.update(dt_seconds, targets or [])

        self.passive_heal(delta_time)

    def draw(self, screen, camera, color):
        screen_rect = camera.apply(self.rect)
        pygame.draw.rect(screen, color, screen_rect)

    def passive_heal(self, delta_time):
        dt_seconds = delta_time / 1000

        if self.invuln_timer > 0:
            self.invuln_timer -= dt_seconds
            if self.invuln_timer < 0:
                self.invuln_timer = 0.0

        if self.current_health < self.get_stat("health"):
            self.regen_timer += dt_seconds
            if self.regen_timer >= self.regen_time:
                self.heal(self.regen_amt)
                self.regen_timer = 0.0