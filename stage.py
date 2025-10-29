import sys
import pygame
import UI

def normal(attempt, row, col, correct, effect, game, board):
    Type = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0, Type, row, col, correct, effect, game, board
        if correct != -1 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Type = 0
                row = 0
                col = 0
                correct = -1
                game.random()
                print(game.get_answer())  # For testing purposes; remove or comment out in production))
                UI.reset_game()
                board.reset()
            elif event.key == pygame.K_RETURN:
                game.random()
                print(game.get_answer())  
                row = 0
                col = 0
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
    board.draw(UI.screen)
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
    return 1, Type, row, col, correct, effect, game, board

def survive(Round, attempt, row, col, correct, effect, game, board):
    Type = 2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0, Type, Round, row, col, correct, effect, game, board
        if correct != -1 and event.type == pygame.KEYDOWN:
            if correct == 0:
                if event.key == pygame.K_ESCAPE:
                    Type = 0
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    game.random()
                    print(game.get_answer()) 
                    Round = 1
                    row = 0
                    col = 0
                    correct = -1
                    UI.reset_game()
                    board.reset()
            elif correct == 1:
                if event.key == pygame.K_RETURN:
                    Round += 1
                    game.random()
                    print(game.get_answer())  
                    row = 0
                    col = 0
                    correct = -1
                    UI.reset_game()
                    board.reset()
                elif event.key == pygame.K_ESCAPE:
                    correct = 0
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

    message = f"Round: {Round}"

    message_text = UI.GAME_OVER_FONT.render(message, True, UI.BLACK)
    message_rect = message_text.get_rect(center=(UI.SCREEN_WIDTH // 2, 40))
    UI.screen.blit(message_text, message_rect)

    UI.draw_grid()
    board.draw(UI.screen)
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

    elif correct == 1:
        UI.draw_finish_round_screen_survival(Round)
    elif correct == 0:
        UI.draw_game_over_screen_survival(game.get_answer(), Round)
    return 1, Type, Round, row, col, correct, effect, game, board

def timed_mode(attempt, row, col, correct, effect, game, board, start_time_ticks, total_duration_sec, final_sec):
    Type = 3

    remaining_sec = 0
    if final_sec == 0:
        current_ticks = pygame.time.get_ticks()
        elapsed_sec = (current_ticks - start_time_ticks) // 1000
        remaining_sec = total_duration_sec - elapsed_sec
        if remaining_sec <= 0:
            remaining_sec = 0
            correct = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0, Type, start_time_ticks, final_sec, row, col, correct, effect, game, board
        if correct != -1 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Type = 0
                row = 0
                col = 0
                final_sec = 0
                game.random()
                print(game.get_answer())  
                correct = -1
                UI.reset_game()
                board.reset()
            elif event.key == pygame.K_RETURN:
                final_sec = 0
                game.random()
                print(game.get_answer()) 
                start_time_ticks = pygame.time.get_ticks()
                row = 0
                col = 0
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
    board.draw(UI.screen)

    minutes = 0
    seconds = 0
    if final_sec != 0:
        minutes = final_sec // 60
        seconds = final_sec % 60
    else:
        minutes = remaining_sec // 60
        seconds = remaining_sec % 60
    timer_str = f"{minutes:02d}:{seconds:02d}"
    timer_text = UI.TIMER_FONT.render(timer_str, True, UI.BLACK) 
    timer_rect = timer_text.get_rect(center=(UI.SCREEN_WIDTH // 2, 30))
    UI.screen.blit(timer_text, timer_rect)

    if effect != 0:
        UI.update_effect(UI.guesses[row], effect)
        if UI.guesses[row][0].flip.is_flip == False and effect == 1:
            effect = 0
            if correct == 0 and row < attempt - 1:
                row += 1
                correct = -1
                col = 0
                word = ""
            elif correct == 1:
                final_sec = remaining_sec
        elif UI.guesses[row][0].shake.is_shaking == False and effect == 2:
            effect = 0

    elif correct == 1 or correct == 0:
        UI.draw_timed_game_over_screen(correct, game.get_answer(), seconds)
    return 1, Type, start_time_ticks, final_sec, row, col, correct, effect, game, board