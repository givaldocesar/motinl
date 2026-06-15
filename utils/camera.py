class Camera:
    def __init__(self, center, radius=10):
        self.radius = radius
        self.x_center = center[0] if (center is not None and len(center) > 0) else 0.0
        self.y_center = center[1] if (center is not None and len(center) > 1) else 0.0
        self.x_min, self.x_max = self.x_center - self.radius, self.x_center + self.radius
        self.y_min, self.y_max = self.y_center - self.radius, self.y_center + self.radius
    
    @property
    def center(self):
        return [self.x_center, self.y_center]
    
    def point_is_offscreen(self, point):
        x = point[0]
        y = point[1] if len(point) > 1 else 0.0

        margin_x = (self.x_max - self.x_min) * 0.1
        margin_y = (self.y_max - self.y_min) * 0.1

        in_margin_x = (x < self.x_min + margin_x) or (x > self.x_max - margin_x)
        in_margin_y = (y < self.y_min + margin_y) or (y > self.y_max - margin_y)
        return in_margin_x or in_margin_y

    def set_center(self, point):
        self.x_center = point[0] if (point is not None and len(point) > 0) else 0.0
        self.y_center = point[1] if (point is not None and len(point) > 1) else 0.0
        self.x_min, self.x_max = self.x_center - self.radius, self.x_center + self.radius
        self.y_min, self.y_max = self.y_center - self.radius, self.y_center + self.radius
