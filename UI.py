from itertools import filterfalse
from pickle import FALSE
import pygame
from UI_cell import cell
from Button import Button

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

GRID_SIZE = 5
CELL_SIZE = 60
CELL_PADDING = 7 
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
TIMER_FONT = pygame.font.Font(None, 36)

def draw_menu_screen():
    menu = [
        Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2, 250, 60, "NORMAL MODE"),
        Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 70, 250, 60, "SURVIVAL MODE"),
        Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 140, 250, 60, "TIMED MODE")
    ]
    mouse_pos = pygame.mouse.get_pos()
    for button in menu:
        button.update(mouse_pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0, -1
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(menu)):
                if menu[i].is_clicked(mouse_pos):
                    return 1, i + 1
    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("WORDLE", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)

    for button in menu:
        button.draw(screen, )
    return 1, 0


def draw_game_over_screen(player_won, answer):
    screen.blit(overlay_surface, (0, 0)) 

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
        message = "THE ANSWER IS: " + answer
        answer_text = RESTART_FONT.render(message, True, WHITE)
        answer_rect = answer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(answer_text, answer_rect) 

    restart_message = "ENTER TO RESTART"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)
    
    restart_message = "ESC TO BACK TO MENU"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
    screen.blit(restart_text, restart_rect)
    
def draw_game_over_screen_survival(answer, round):
    screen.blit(overlay_surface, (0, 0))
    message = "GAME OVER!"
    message_color = RED

    message_text = GAME_OVER_FONT.render(message, True, message_color)
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(message_text, message_rect)

    message = "THE ANSWER IS: " + answer
    answer_text = RESTART_FONT.render(message, True, WHITE)
    answer_rect = answer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(answer_text, answer_rect) 

    message = "YOU REACHED ROUND: " + str(round)
    round_text = RESTART_FONT.render(message, True, WHITE)
    round_rect = round_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(round_text, round_rect)

    restart_message = "ENTER TO RESTART"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

    
    restart_message = "ESC TO BACK TO MENU"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(restart_text, restart_rect)

def draw_finish_round_screen_survival(round):
    screen.blit(overlay_surface, (0, 0)) 
    message = "WELL DONE!"
    message_color = GREEN

    message_text = GAME_OVER_FONT.render(message, True, message_color)
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(message_text, message_rect)

    message = "YOU COMPLETED ROUND: " + str(round)
    round_text = RESTART_FONT.render(message, True, WHITE)
    round_rect = round_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(round_text, round_rect)

    restart_message = "ENTER TO CONTINUE"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

    restart_message = "ESC TO END"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(restart_text, restart_rect)

def draw_timed_game_over_screen(player_won, answer, remaining_sec):
    screen.blit(overlay_surface, (0, 0)) 

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
        message = f"TIME'S UP!"
        time_text = RESTART_FONT.render(message, True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
        screen.blit(time_text, time_rect)

        message = "THE ANSWER IS: " + answer
        answer_text = RESTART_FONT.render(message, True, WHITE)
        answer_rect = answer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(answer_text, answer_rect) 

    else:
        message = f"TIME REMAINING: {remaining_sec} SEC"
        time_text = RESTART_FONT.render(message, True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(time_text, time_rect)

    restart_message = "ENTER TO RESTART"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(restart_text, restart_rect)

    restart_message = "ESC TO BACK TO MENU"
    restart_text = RESTART_FONT.render(restart_message, True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(restart_text, restart_rect)