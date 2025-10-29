from encodings.punycode import T
import sys
import time
from word import words
from gameplay import gameplay
from UI_keyboard import Keyboard
from stage import normal, survive, timed_mode
import UI
import pygame

def main():
    word_list = words()
    try:
        with open("data.txt", "r") as f:
            word_list.load_from_stream(f)
    except FileNotFoundError:
        print("!!! Error: Cannot find 'words.txt'!")
    except Exception as e:
        print(f"!!! Other Error: {e}")

    game = gameplay(word_list)
    print(game.get_answer())  
    running = True
    attempt = 6
    row = 0
    col = 0
    pygame.display.set_caption(UI.SCREEN_TITLE)
    correct = -1
    effect = 0
    word = ""
    board = Keyboard()
    Type = 0
    Round = 1
    total_duration_sec = 30
    start_time_ticks = 0 
    final_sec = 0
    while running:
        UI.screen.fill(UI.BACKGROUND_COLOR)
        if Type == 0:
            running, Type = UI.draw_menu_screen()
            pygame.display.flip()
            if Type == 3:
                start_time_ticks = pygame.time.get_ticks()
            continue
        if Type == 1:
            running, Type, row, col, correct, effect, game, board = normal(attempt, row, col, correct, effect, game, board)
        elif Type == 2:
            running, Type, Round, row, col, correct, effect, game, board = survive(Round, attempt, row, col, correct, effect, game, board)
        elif Type == 3:
            running, Type, start_time_ticks, final_sec, row, col, correct, effect, game, board = timed_mode(attempt, row, col, correct, effect, game, board, start_time_ticks, total_duration_sec, final_sec)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()