from cmath import rect
import pygame
from UI import SCREEN_WIDTH, BLACK, WHITE, GREY, GREEN, YELLOW, GREY
from Button import Button

class Keyboard:
    def __init__(self, start_y=500, key_size=40, key_padding=10):
        self.layout = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "DZXCVBNME"
        ]
        self.start_y = start_y
        self.key_size = key_size
        self.key_padding = key_padding
        self.lines = [
            [
                Button(
                    ((SCREEN_WIDTH - (len(self.layout[row]) * key_size + (len(self.layout[row]) - 1) * key_padding)) // 2) + col * (key_size + key_padding), 
                    start_y + row * (key_size + key_padding),
                    key_size,
                    key_size,
                    self.layout[row][col], 
                ) 
                for col in range(len(self.layout[row]))
            ] 
            for row in range(3)
        ]
        enter_width = len("ENTER") * 20
        self.lines[2][-1].text = "ENTER"
        self.lines[2][-1].rect.width = enter_width

        delete_width = len("DEL") * 20
        self.lines[2][0].text = "DEL"
        self.lines[2][0].rect.width = delete_width
        self.lines[2][0].rect.x = self.lines[2][1].rect.x - key_padding - delete_width

    def draw(self, screen):
        for i in range (3):
            for j in range(len(self.layout[i])):
                self.lines[i][j].draw(screen)

    def update_key_color(self, guess):
        for i in range (5):
            for j in range(3):
                for k in range (self.layout[j].__len__()):
                    if guess[i].char == self.lines[j][k].text:
                        self.lines[j][k].text_color = WHITE
                        if guess[i].color == GREEN:
                            self.lines[j][k].bg_color = GREEN
                        elif guess[i].color == YELLOW and self.lines[j][k].bg_color != GREEN:
                            self.lines[j][k].bg_color = YELLOW
                        elif guess[i].color == GREY and self.lines[j][k].bg_color == WHITE:
                            self.lines[j][k].bg_color = GREY
                        break

    def reset(self):
        for line in self.lines:
            for char in line:
                char.bg_color = WHITE
                char.text_color = BLACK