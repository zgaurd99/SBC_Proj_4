import pygame
from ui.button import UIButton


class MenuState:
    def __init__(self, screen_width, screen_height, assets, on_play, offset_x, offset_y, int_scale):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.assets = assets
        self.on_play = on_play
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.int_scale = int_scale

        self.font = pygame.font.Font(
            "assets/fonts/Kenney Future.ttf",
            int(screen_height * 0.05)
        )

        self.buttons = []
        self._build_buttons()

    def _build_buttons(self):
        W = self.screen_width
        H = self.screen_height

        btn_w = self.assets.get("btn_blue").get_width()
        btn_h = self.assets.get("btn_blue").get_height()
        clip_w = int(btn_w * 0.1)  # how much bleeds off edge
        clip_h = int(btn_h * 0.1)  # how much bleeds off edge

        self.buttons.append(UIButton(
            x=-clip_w, y=int(H * 0.15),
            surface=self.assets.get("btn_blue"),
            label="Powerups",
            font=self.font,
            callback=lambda: print("Powerups")
        ))

        self.buttons.append(UIButton(
            x=-clip_w, y=int(H * 0.40),
            surface=self.assets.get("btn_red"),
            label="Gear",
            font=self.font,
            callback=lambda: print("Gear")
        ))

        self.buttons.append(UIButton(
            x=W - btn_w + clip_w, y=int(H * 0.25),
            surface=self.assets.get("btn_yellow"),
            label="Punishments",
            font=self.font,
            callback=lambda: print("Punishments")
        ))

        self.buttons.append(UIButton(
            x=int(W * 0.5) - self.assets.get("btn_green").get_width() // 2,
            y=H - btn_h + clip_h,
            surface=self.assets.get("btn_green"),
            label="PLAY",
            font=self.font,
            callback=self.on_play
        ))

        self.buttons.append(UIButton(
            x=(W - self.assets.get("gear").get_width()) * 0.975,
            y=(H - self.assets.get("gear").get_height()) * 0.95,
            surface=self.assets.get("gear"),
            label="",
            font=self.font,
            callback=lambda: print("Settings")
        ))

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            virtual_pos = (
                (event.pos[0] - self.offset_x) // self.int_scale,
                (event.pos[1] - self.offset_y) // self.int_scale
            )
            for button in self.buttons:
                button.handle_click(virtual_pos)

    def update(self, delta_time):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for button in self.buttons:
            button.draw(screen)