#import

class Word:
    def __init__(self, answer):
        self.answer = answer
        self.guessed = [False for i in range(len(answer))]

    # @return: true if letter was found
    def guess(self,letter):
        ret = False
        for i in range(len(self.answer)):
            if self.answer[i] == letter:
                ret = True
                self.guessed[i] = True
        return ret

    def __len__(self):
        return len(self.answer)

    def __str__(self):
        return ' '.join([ (self.answer[i] if self.guessed[i] else '_') for i in range(len(self.answer)) ])
        
    
