import pygame

class flip:
    def __init__(self):
        self.is_flip = 0
        self.progress = 0
        self.speed = 20
        self.color = (255, 255, 255)
    def update(self, color):
        self.progress += self.speed
        if self.progress >= 90:
            self.color = color
        if self.progress >= 180:
            self.progress = 0
            self.color = (255, 255, 255)
            self.is_flip = False

class shake:
    def __init__(self):
        self.is_shaking = False
        self.shake_timer = 0
        self.shake_duration = 20
        self.shake_offsets = [-4, 4, -4, 4, -2, 2, 0]
    def update(self):
        if self.is_shaking:
            self.shake_timer += 1
            if self.shake_timer >= self.shake_duration:
                self.is_shaking = False
                self.shake_timer = 0