# stdlib
import getpass, re
import sys, time

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
        time.sleep(0.5)
        w = getpass.getpass("Word: ")
        self.word = word.Word(w)
        print("Pass the computer to the players")
        time.sleep(1)
        while(1):
            # Print the gameboard
            print("\n   %s/8   "%self.strikes+''.join(['-' if self.usedletters[i] else chr(i+65) for i in range(26)]))
            lines=getDrawing(self.strikes).split('\n')
            lines[3] += '    '+str(self.word)
            print('\n'.join(lines))

            time.sleep(0.2)
            # Game over checks
            if self.word.isWordGuessed():
                return True
            elif self.strikes == 8:
                return False

            time.sleep(0.5)
            # input
            a=None
            while(1):
                sys.stdout.write("Choose a letter, * to guess, or & to quit: ")
                a=getch.getch().upper()
                if re.match(r'[\w]',a):
                    if self.usedletters[ord(a)-65]:
                        print("You already used that!")
                        continue
                    else:
                        sys.stdout.write(a) # echo the letter
                        break
                elif a=='&': # Quit
                    return None
                elif a=='*':
                    self.guessWord()
                    a=None
                elif a==chr(3):
                    raise KeyboardInterrupt
                print("Not a valid letter")
            if a!=None:
                ind = ord(a)-65
                self.usedletters[ind]=True
                result = self.word.guess(a)
                if(result):
                    print("\nYou got one!")
                else:
                    print("\nNope!")
                    self.strikes += 1
            # gameloop
        #end of play()


    def guessWord():
        pass


    def playAgain(self,result):
        if result != None:
            print("Game over! Looks like you "+('won' if result else 'lost')+"!")
        i = raw_input("Want to play again? (Y/n) ")
        # first letter of 'no' and 'quit'
        if i[0] in 'NnQq':
            return False
        return True

if __name__=="__main__":
    g=HangmanGame()
    while(g.playAgain(g.play())):
        pass
    raise SystemExit

