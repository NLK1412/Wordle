from encodings.punycode import T
import sys
from word import words
from gameplay import gameplay
from UI_keyboard import Keyboard
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
    print(game.get_answer())  # For testing purposes; remove or comment out in production)
    running = True
    attempt = 6
    row = 0
    col = 0
    pygame.display.set_caption(UI.SCREEN_TITLE)
    correct = -1
    effect = 0
    word = ""
    board = Keyboard()
    while running:
        UI.screen.fill((255, 255, 255))
        UI.draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if effect != 0:
                continue
            if correct != -1 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    game = gameplay(word_list)
                    print(game.get_answer())  # For testing purposes; remove or comment out in production)
                    row = 0
                    col = 0
                    word = ""
                    correct = -1
                    UI.reset_game()
                    board.reset()
            elif correct == -1 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if col == 0:
                        continue
                    col -= 1
                    UI.guesses[row][col].char = ""
                elif event.key == pygame.K_RETURN:
                    if col < 5:
                        continue
                    correct = game.play(word := "".join([UI.guesses[row][i].char for i in range(5)]))
                    if correct == -1:
                        UI.update_effect(UI.guesses[row], 2)
                        effect = 2
                    else:
                        UI.update_color(UI.guesses[row], game.get_check())
                        board.update_key_color(UI.guesses[row])
                        UI.update_effect(UI.guesses[row], 1)
                        effect = 1

                elif col < 5 and event.unicode.isalpha():
                    UI.guesses[row][col].char = event.unicode.upper()
                    col += 1

        UI.draw_grid()
        board.draw()
        if effect != 0:
            UI.update_effect(UI.guesses[row], effect)
            if UI.guesses[row][0].flip.is_flip == False and effect == 1:
                effect = 0
                if correct == 0 and row < attempt - 1:
                    row += 1
                    correct = -1
                    col = 0
                    word = ""
            elif UI.guesses[row][0].shake.is_shaking == False and effect == 2:
                effect = 0

        elif correct == 1 or correct == 0:
            UI.draw_game_over_screen(correct, game.get_answer())
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()