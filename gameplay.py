from word import word

class gameplay:
    def __init__(self, list):
        self.__words = list
        self.__answer = list.random()
        self.__guess = ""
        self.__check = []
    def __check_word_syntax(self):
        return (len(self.__guess) == 5 or self.__guess.isalpha() == True)
    def __make_guess(self):
        self.__check.clear()
        correct = 0
        for i in range(5):
            if self.__guess[i] == self.__answer[i]:
                self.__check.append(1)
                correct += 1
            elif self.__guess[i] in self.__answer:
                self.__check.append(0)
            else:
                self.__check.append(-1)
        if correct == 5:
            return True
        for i in range(5):
            if self.__check[i] == 1:
                continue
            for j in range(5):
                if i != j and self.__guess[i] == self.__answer[j]:
                    if self.__check[j] != 1:
                        self.__check[i] = 0
                else:
                    self.__check[i] = -1
        return False
    def get_check(self):
        return self.__check
    def get_answer(self):
        return self.__answer
    def get_list(self, num):
        self.__words.list_elements(num)
    def start_game(self):
        attempts = 6
        while attempts > 0:
            print("Enter your 5-letter guess:")
            self.__guess = input().upper()
            if not self.__check_word_syntax():
                print("Invalid input. Please enter a 5-letter word.")
                continue
            if self.__words.check(self.__guess) == False:
                print("Word not in list. Please try again.")
                continue
            self.__guess.upper()
            if self.__make_guess():
                print("Congratulations! You've guessed the word:", self.__answer)
                return
            print("Feedback:", self.get_check())
            attempts -= 1
            print(f"Attempts remaining: {attempts}")
        print("Sorry, you've run out of attempts. The correct word was:", self.__answer)