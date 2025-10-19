class word:
    def __init__(self):
        self.__words = []
        self.__n = 0
    def load_from_stream(self, stream):
        print("debug")
        for line in stream:
            temp = line.strip()
            if temp:
                self.__words.append(temp)
                self.__n += 1
    def length(self):
        return self.__n
    def check(self, new_word):
        for x in self.__words:
            if x == new_word:
                return True
        return False
    def write_to_stream(self, load):
        for x in self.__words:
            load.write(x + "\n")
    def __check_word(self, Word):
        if len(Word) != 5:
            return False
        return Word.isalpha()
    def add_new_word(self, Word):
        if not self.check(Word):
            Word = Word.upper()
            self.__words.append(Word)
            self.__n += 1
            return True
        return False
    def list_elements(self, num):
        for i in range(num):
            print(self.__words[i])
    def random(self):
        import random
        return random.choice(self.__words)