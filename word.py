
class Word:
    def __init__(self, answer):
        self.gameOver = False
        if type(answer) == type(self):
            self.answer = answer.answer
            self.guessed = answer.guessed
            return
        self.answer = answer.upper()
        # array of bools, represent if each letter is visible
        # init to false, except auto-mark spaces as true
        # TODO symbol support?
        self.guessed = [answer[i] == ' ' for i in range(len(answer))]

    # @return: true if letter was found
    def guess(self, letter):
        ret = False
        l = letter.upper()
        for i in range(len(self.answer)):
            if self.answer[i] == letter:
                ret = True
                self.guessed[i] = True
        return ret

    def isWordGuessed(self):
        if self.gameOver:
            return True
        for i in range(len(self.answer)):
            if not self.guessed[i]:
                return False
        self.gameOver = True
        return True

    def longGuess(self, g):
        r = (g.upper() == self.answer)
        if r:
            self.gameover = True
        return r

    def __len__(self):
        return len(self.answer)

    def __str__(self):
        return ' '.join([
            (self.answer[i] if self.guessed[i] else '_')
            for i in range(len(self.answer))
        ])
