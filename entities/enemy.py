from entities.entity import Entity
from core.animation import AnimationComponent
import pygame


class Enemy(Entity):
    def __init__(self, x, y, config, virtual_h=240):
        anim_config = config.get("animation")

        if anim_config:
            self.animation = AnimationComponent(
                anim_config["sheet"],
                anim_config["json"]
            )
            # Scale sprite frame to virtual resolution
            base_virtual_h = 240
            sprite_scale = virtual_h / base_virtual_h
            fw, fh = self.animation.frame_size
            config = config.copy()
            config["width"] = max(1, int(fw * sprite_scale))
            config["height"] = max(1, int(fh * sprite_scale))
        else:
            self.animation = None

        super().__init__(x, y, config)

        self.gauge_cost = config["gauge_cost"]
        self.colour = config["colour"]
        self.anger_value = config["gauge_cost"]

    def _get_anim_state(self):
        attack_speed = self.get_stat("attack_speed")
        if self.hit_timer > 0:
            if self.hit_timer > attack_speed * 0.5:
                return "Attacking"
            return "Cooldown"
        return "Waiting"

    def update(self, target_rect, delta_time):
        if self.hit_timer > 0:
            self.hit_timer -= delta_time

        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            if self.animation:
                self.animation.set_state("Waiting")
                self.animation.update(delta_time * 1000)
            return

        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        self.move(dx, dy)

        if self.animation:
            self.animation.set_state(self._get_anim_state())
            self.animation.update(delta_time * 1000)

    def draw(self, screen, camera, color=None):
        if self.animation:
            frame = self.animation.current_frame
            screen_rect = camera.apply(self.rect)
            scaled = pygame.transform.scale(
                frame,
                (self.rect.width, self.rect.height)
            )
            screen.blit(scaled, screen_rect)
        else:
            if color is None:
                color = self.colour
            super().draw(screen, camera, color)