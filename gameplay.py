from calendar import c
from word import words

class gameplay:
    def __init__(self, list):
        self.__words = list
        self.__answer = list.random()
        self.__check = []
        self.guess = ""
    def random(self):
        self.__answer = self.__words.random()
    def __make_guess(self):
        self.__check.clear()
        correct = 0
        for i in range(5):
            if self.__guess[i] == self.__answer[i]:
                self.__check.append(1)
                correct += 1
            else:
                self.__check.append(0)
        if correct == 5:
            return True
        check = [0, 0, 0, 0, 0]
        for i in range(5):
            if self.__check[i] == 1:
                check[i] = 1
                continue
            for j in range(5):
                if i != j and self.__guess[i] == self.__answer[j]:
                    if check[j] != 1:
                        self.__check[i] = 0
                        check[j] = 1
                        break
                else:
                    self.__check[i] = -1
        return False
    def get_check(self):
        return self.__check
    def get_answer(self):
        return self.__answer
    def get_list(self, num):
        self.__words.list_elements(num)
    def play(self, word):
        self.__guess = word
        if self.__words.check(self.__guess) == False:
            return -1
        elif self.__make_guess() == True: return 1
        else: return 0