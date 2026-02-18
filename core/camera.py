class Camera:
    def __init__(self, screen_width, screen_height, world_width = None, world_height = None):
        
        # initializing screen dimensions
        self.S_W = screen_width
        self.S_H = screen_height
        
        #initializing world dimensions
        self.W_W = world_width
        self.W_H = world_height
        
        self.x = 0
        self.y = 0
    
    def update(self, target_rect):
        """
        Camera centres on target
        """
        
        self.x = target_rect.centerx - self.S_W // 2
        self.y = target_rect.centery - self.S_H // 2

        if self.W_W is not None:
            self.x = max(0, min(self.x, self.W_W - self.S_W))
        
        if self.W_H is not None:
            self.y = max(0, min(self.y, self.W_H - self.S_H))

    def apply(self, rect):
        """
        Converts the world rect to screen rect
        """
        return rect.move(-self.x, -self.y)