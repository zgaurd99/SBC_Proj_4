import pygame

class HUD:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.padding = max(3, int(screen_height * 0.025))

        # Virtual resolution scale factor (base virtual height = 300)
        self.scale = screen_height / 300

        # Font
        self.font = pygame.font.Font(
            "assets/fonts/04B_30__.TTF",
            max(8, int(screen_height * 0.07))
        )
        self.timer_colour = (220, 195, 120)

        # Load tilesheet
        sheet = pygame.image.load("assets/ui/Health_tilesheet.png").convert_alpha()

        # Extract raw tiles
        base_left_raw  = sheet.subsurface(pygame.Rect(1,  0, 16, 32))
        base_mid_raw   = sheet.subsurface(pygame.Rect(19, 0,  4, 32))
        base_right_raw = sheet.subsurface(pygame.Rect(25, 0, 16, 32))
        fill_mid_raw   = sheet.subsurface(pygame.Rect(43, 0,  4, 32))
        fill_cap_raw   = sheet.subsurface(pygame.Rect(49, 0,  2, 32))

        # Scale all tiles by virtual resolution factor
        def s(surf, w, h):
            return pygame.transform.scale(
                surf,
                (max(1, int(w * self.scale)), max(1, int(h * self.scale)))
            )

        self.base_left  = s(base_left_raw,  16, 32)
        self.base_mid   = s(base_mid_raw,    4, 32)
        self.base_right = s(base_right_raw, 24, 32)
        self.fill_mid   = s(fill_mid_raw,    4, 32)
        self.fill_cap   = s(fill_cap_raw,    2, 32)

        # Scaled tile dimensions
        self.base_left_w  = self.base_left.get_width()
        self.base_right_w = self.base_right.get_width()
        self.base_mid_w   = self.base_mid.get_width()
        self.fill_cap_w   = self.fill_cap.get_width()
        self.fill_mid_w   = self.fill_mid.get_width()
        self.tile_h       = self.base_left.get_height()
        self.fill_h       = self.fill_mid.get_height()

        # HP per tile segment
        self.hp_per_base_cap = 11
        self.hp_per_base_mid = 4
        self.hp_per_fill_cap = 2
        self.hp_per_fill_mid = 4

        # Pixel anchors (scaled)
        self.fill_offset_x = int(6 * self.scale)
        self.fill_offset_y = int(5 * self.scale)
        self.fill_right_inset = int((16-10) * self.scale)  # base right tile inner x=10

        self.start_ticks = pygame.time.get_ticks()

    def _build_base_bar(self, max_hp):
        """Compute how many middle tiles needed for base bar given max HP."""
        inner_hp = max(0, max_hp - self.hp_per_base_cap * 2)
        mid_count = max(1, -(-inner_hp // self.hp_per_base_mid))  # ceiling div
        return mid_count

    def _bar_total_w(self, mid_count):
        return self.base_left_w + self.base_mid_w * mid_count + self.base_right_w

    def draw(self, screen, game_state):
        self._draw_hp_bar(screen, game_state)
        self._draw_timer(screen)

    def _draw_hp_bar(self, screen, game_state):
        player = game_state.player
        max_hp = player.get_stat("health")
        current_hp = max(0.0, player.current_health)

        x = self.padding
        y = self.padding

        mid_count = self._build_base_bar(max_hp)

        # --- Draw base bar ---
        cx = x
        screen.blit(self.base_left, (cx, y))
        cx += self.base_left_w

        for _ in range(mid_count):
            screen.blit(self.base_mid, (cx, y))
            cx += self.base_mid_w

        screen.blit(self.base_right, (cx, y))

        # --- Compute fill bar bounds ---
        fill_x = x + self.fill_offset_x
        fill_y = y

        # Right bound: base right tile's inner pixel x=10
        base_right_x = x + self.base_left_w + self.base_mid_w * mid_count
        fill_max_right = base_right_x + self.base_right_w - self.fill_offset_x - int(2 * self.scale)
        fill_max_w = fill_max_right - fill_x

        # --- Compute fill width from current HP ---
        # Total fill width maps linearly from 0 to fill_max_w over 0 to max_hp
        fill_w = int(fill_max_w * (current_hp / max_hp)) if max_hp > 0 else 0

        if fill_w <= 0:
            return

        # --- Draw fill bar ---
        # Left cap
        left_cap_w = min(self.fill_cap_w, fill_w)
        if left_cap_w > 0:
            clipped = self.fill_cap.subsurface(pygame.Rect(0, 0, left_cap_w, self.fill_h))
            screen.blit(clipped, (fill_x, fill_y))

        # Middle tiles
        mid_x = fill_x + self.fill_cap_w
        remaining = fill_w - self.fill_cap_w

        if remaining > 0:
            full_mids = remaining // self.fill_mid_w
            partial_w = remaining % self.fill_mid_w

            for _ in range(full_mids):
                screen.blit(self.fill_mid, (mid_x, fill_y))
                mid_x += self.fill_mid_w

            if partial_w > 0:
                clipped_mid = self.fill_mid.subsurface(
                    pygame.Rect(0, 0, partial_w, self.fill_h)
                )
                screen.blit(clipped_mid, (mid_x, fill_y))
                mid_x += partial_w

        # Right cap — only if there's room
        right_fill_x = fill_x + fill_w - self.fill_cap_w
        if fill_w >= self.fill_cap_w * 2 and right_fill_x > fill_x + self.fill_cap_w:
            screen.blit(self.fill_cap, (right_fill_x, fill_y))

    def _draw_timer(self, screen):
        elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        minutes = elapsed // 60
        seconds = elapsed % 60

        text = self.font.render(f"{minutes:02d}:{seconds:02d}", True, self.timer_colour)
        x = self.screen_width - text.get_width() - self.padding
        y = self.padding
        screen.blit(text, (x, y))