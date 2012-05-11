# stdlib
import getpass
# libraries
import getch
# program
import word

def getDrawing(strikes):
    armarray=["   ","   "," | "," | ","\\| ","\\|/"]
    legarray=["   ","/  ","/ \\","/ \\"]
    def head(s):
        return " x " if s==8 else (" o " if s>0 else "   ")
    def arms(s):
        return armarray[s if s<=4 else 5]
    def body(s):
        return " | " if s>=3 else "   "
    def legs(s):
        return legarray[s-5 if s>5 else 0]
    
    return """\
  _____   
 |     |  \n"""+head(strikes)+\
"""    |  \n"""+arms(strikes)+\
"""    |  \n"""+body(strikes)+\
"""    |  \n"""+legs(strikes)+\
"""    |  
     __|__"""


class HangmanGame:
    def __init__(self):
        self.usedletters = [False for i in range(26)]
        self.word = None
        self.strikes = 0

    def play(self):
        print('\n')
        print("Please pass the computer to the word-maker.")
        w = getpass.getpass("Word: ")
        self.word = word.Word(w)
        print("Pass the computer to the players")
        while(1):
            print("\n   %s/8   "%self.strikes+''.join(['-' if self.usedletters[i] else chr(i+65) for i in range(26)]))
            lines=getDrawing(self.strikes).split('\n')
            lines[3] += '    '+str(self.word)
            print('\n'.join(lines))
            a=""
            while(1):
                a=getch.getch("Choose a letter, or * to guess: ")
                if len(a) != 1:
                    print("Only one letter, please")

if __name__=="__main__":
    g=HangmanGame()
    g.play()
    while(g.playAgain()):
        g.play()
    raise SystemExit

