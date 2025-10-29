from tkinter import SE
import pygame
class Button:
    def __init__(self, x, y, width, height, text, font_size=30, bg_color= (255, 255, 255), text_color=(0, 0, 0), hover_color = (0, 0, 0), text_hover_color = (255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text_hover_color = text_hover_color
        self.is_hovering = 0
        self.font = pygame.font.SysFont('arial', self.font_size)

    def update(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen):
        current_bg = self.hover_color if self.is_hovering else self.bg_color
        current_text_color = self.text_hover_color if self.is_hovering else self.text_color

        pygame.draw.rect(screen, current_bg, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = self.font.render(self.text, True, current_text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)