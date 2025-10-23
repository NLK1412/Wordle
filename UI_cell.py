import pygame
import math
from UI_effects import flip
from UI_effects import shake

class cell:
    def __init__(self, x, y, char, size, line, color):
        self.x = x
        self.y = y
        self.char = char
        self.size = size
        self.color = color
        self.char_color = (0, 0, 0)
        self.line = line
        self.flip = flip()
        self.shake = shake()
    def draw(self, screen, char_size):
        if self.flip.is_flip:
            x, y, size = self.x, self.y, self.size
            scale = abs(math.cos(math.radians(self.flip.progress)))

            cur_height = size * scale
            cur_y = y + (size - cur_height) // 2

            pygame.draw.rect(screen, self.flip.color, (x, cur_y, size, cur_height))

            if cur_height > 0:
                pygame.draw.rect(screen, self.flip.color, (x, cur_y, size, cur_height), 2)

        elif self.shake.is_shaking:
            current_offset_x = 0
            if self.shake.is_shaking:
                offset_index = self.shake.shake_timer % len(self.shake.shake_offsets)
                current_offset_x = self.shake.shake_offsets[offset_index]

            draw_x = self.x + current_offset_x
            draw_y = self.y

            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.size, self.size))
            pygame.draw.rect(screen, self.line, (draw_x, draw_y, self.size, self.size), 2)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
            pygame.draw.rect(screen, self.line, (self.x, self.y, self.size, self.size), 2)
        if self.char != "":
            FONT = pygame.font.SysFont('arial', char_size)
            text_surface = FONT.render(self.char, True, self.char_color)
            text_rect = text_surface.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            screen.blit(text_surface, text_rect)
        