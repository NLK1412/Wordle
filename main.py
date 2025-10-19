import sys
from word import word
from gameplay import gameplay

def main():
    word_list = word()
    try:
        with open("data.txt", "r") as f:
            word_list.load_from_stream(f)
    except FileNotFoundError:
        print("!!! Error: Cannot find 'words.txt'!")
    except Exception as e:
        print(f"!!! Other Error: {e}")
    game = gameplay(word_list)
    print("Welcome to the Wordle!")
    game.start_game()
if __name__ == "__main__":
    main()