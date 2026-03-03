class Camera:
    def __init__(self, screen_width, screen_height, world_width=None, world_height=None):
        # initializing screen dimensions — used to calculate where the camera should center
        self.S_W = screen_width
        self.S_H = screen_height
        # initializing world dimensions — optional, used to clamp the camera within world bounds
        self.W_W = world_width
        self.W_H = world_height
        self.x = 0  # camera's current horizontal offset in world space
        self.y = 0  # camera's current vertical offset in world space

    def update(self, target_rect):
        # called every frame to reposition the camera so the target stays centered on screen
        """Camera centres on target"""
        self.x = target_rect.centerx - self.S_W // 2
        self.y = target_rect.centery - self.S_H // 2

        # clamp horizontal position so the camera doesn't scroll past the world's left or right edge
        if self.W_W is not None:
            self.x = max(0, min(self.x, self.W_W - self.S_W))

        # clamp vertical position so the camera doesn't scroll past the world's top or bottom edge
        if self.W_H is not None:
            self.y = max(0, min(self.y, self.W_H - self.S_H))

    def apply(self, rect):
        # converts a world-space rect to screen-space by offsetting against the camera's position
        # use this on any entity or object before drawing it to the screen
        """Converts the world rect to screen rect"""
        return rect.move(-self.x, -self.y)