from itertools import filterfalse
from pickle import FALSE
import pygame
from UI_cell import cell

import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Wordle Game"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND_COLOR = (255, 255, 255)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Các hằng số cho lưới
GRID_SIZE = 5
CELL_SIZE = 60
CELL_PADDING = 7 # Khoảng cách giữa các ô
GRID_START_X = (SCREEN_WIDTH - (GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_PADDING)) // 2
GRID_START_Y = 80

guesses = [[cell(GRID_START_X + col * (CELL_SIZE + CELL_PADDING), GRID_START_Y + row * (CELL_SIZE + CELL_PADDING), "", CELL_SIZE, GREY, WHITE) for col in range(GRID_SIZE)] for row in range(6)]
user_input = ""

def draw_grid():
    for row in range(6):
        for col in range(GRID_SIZE):
            guesses[row][col].draw(screen, 48)

def update_color(row, check_word):
    for col in range(5):
        if(check_word[col] == 1):
            row[col].color = GREEN
            row[col].char_color = WHITE
        elif(check_word[col] == 0):
            row[col].color = YELLOW
            row[col].char_color = WHITE
        elif(check_word[col] == -1):
            row[col].color = GREY
            row[col].char_color = WHITE

def update_effect(row, flag):
    if flag == 1:
        for col in range(5):
            row[col].flip.is_flip = True
            row[col].flip.update(row[col].color)
    elif flag == 2:
        for col in range(5):
            row[col].shake.is_shaking = True
            row[col].shake.update()

def reset_game():
    for row in range(6):
        for col in range(GRID_SIZE):
            guesses[row][col].char = ""
            guesses[row][col].color = WHITE
            guesses[row][col].char_color = BLACK
            guesses[row][col].line = GREY


OVERLAY_COLOR = (0, 0, 0, 100) 

overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
overlay_surface.fill(OVERLAY_COLOR)

GAME_OVER_FONT = pygame.font.Font(None, 72)
RESTART_FONT = pygame.font.Font(None, 36)

def draw_game_over_screen(player_won, answer):
    # 1. Vẽ lớp phủ làm mờ
    screen.blit(overlay_surface, (0, 0)) # Vẽ lớp phủ lên toàn bộ màn hình

    # 2. Vẽ thông báo kết quả
    if player_won:
        message = "YOU WIN!"
        message_color = GREEN
    else:
        message = "YOU LOSE!"
        message_color = RED

    message_text = GAME_OVER_FONT.render(message, True, message_color)
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(message_text, message_rect)

    if player_won == False:
        message = "THE ANSWER WAS: " + answer
        answer_text = RESTART_FONT.render(message, True, WHITE)
        answer_rect = answer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(answer_text, answer_rect) 

    restart_message = "PRESS ENTER TO RESTART OR ESC TO QUIT"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)