import pygame
from UI import SCREEN_WIDTH, BLACK, WHITE, GREY, GREEN, YELLOW, GREY, screen
from UI_cell import cell


class Keyboard:
    def __init__(self, start_y=500, key_size=40, key_padding=10):
        self.layout = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        self.start_y = start_y
        self.key_size = key_size
        self.key_padding = key_padding
        self.lines = [
            [
                cell(
                    ((SCREEN_WIDTH - (len(self.layout[row]) * key_size + (len(self.layout[row]) - 1) * key_padding)) // 2) + col * (key_size + key_padding), 
                    start_y + row * (key_size + key_padding), 
                    self.layout[row][col], 
                    key_size, 
                    BLACK, 
                    WHITE
                ) 
                for col in range(len(self.layout[row]))
            ] 
            for row in range(3)
        ]
    def draw(self):
        for i in range (3):
            for j in range(len(self.layout[i])):
                self.lines[i][j].draw(screen, 20)
    def update_key_color(self, guess):
        for i in range (5):
            for j in range(3):
                for k in range (self.layout[j].__len__()):
                    if guess[i].char == self.lines[j][k].char:
                        self.lines[j][k].char_color = WHITE
                        if guess[i].color == GREEN:
                            self.lines[j][k].color = GREEN
                        elif guess[i].color == YELLOW and self.lines[j][k].color != GREEN:
                            self.lines[j][k].color = YELLOW
                        elif guess[i].color == GREY and self.lines[j][k].color == WHITE:
                            self.lines[j][k].color = GREY
                        break
    def reset(self):
        for line in self.lines:
            for char in line:
                char.color = WHITE
                char.char_color = BLACK