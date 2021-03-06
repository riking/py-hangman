#!/usr/bin/python3
# stdlib
import getpass
import re
import sys
import time

# libraries
import getch
import colorama
from colorama import Fore, Back, Style

# program
import word

colorama.init()

WIN = 1
LOSE = 2
CANCEL = 3
QUIT = 4


def getDrawing(strikes):
    armarray = ["   ", "   ", " | ", " | ", "\\| ", "\\|/"]
    legarray = ["   ", "/  ", "/ \\", "/ \\"]

    def head(s):
        return " x " if s == 8 else (" o " if s > 0 else "   ")

    def arms(s):
        return armarray[s if s <= 4 else 5]

    def body(s):
        return " | " if s >= 3 else "   "

    def legs(s):
        return legarray[s - 5 if s > 5 else 0]

    return """\
  _____
 |     |  \n""" + head(strikes) + \
"""    |  \n""" + arms(strikes) + \
"""    |  \n""" + body(strikes) + \
"""    |  \n""" + legs(strikes) + \
"""    |
     __|__"""


class LetterSet:  # TODO: Full support
    def __init__(self, regex, siz):
        self.size = siz
        self.reg = regex.upper()  # force uppercase

    def stringInSet(self, string):
        # start of string, group, plus, end of string
        return re.match(r'^%s+$' % self.reg, string)

    def letterInSet(self, letter):
        return re.match(self.reg, letter)

LetterSet.alpha = LetterSet(r'[A-Z ]', 26)


class HangmanGame:
    def __init__(self):
        # self.usedletters = [False for i in range(26)]
        self.set = LetterSet.alpha
        self.word = None
        self.strikes = 0

    def play(self):

        print('\n')

        print(Style.BRIGHT + Fore.GREEN + "Please pass the computer to the word-maker." + Style.RESET_ALL)
        time.sleep(0.5)
        w = getpass.getpass("Word: ")
        self.word = word.Word(w)
        # Detect type of word
        if not self.set.stringInSet(self.word.answer):
            print("\n\nPlease only use alphabetical words")
            return CANCEL
        self.usedletters = [False for i in range(LetterSet.alpha.size)]

        print(Style.BRIGHT + Fore.GREEN + "Pass the computer to the players" + Fore.RESET)
        time.sleep(1)

        while(1):
            # Game over checks
            if self.word.isWordGuessed():
                print(Fore.WHITE + Back.GREEN + "You win!" + Style.RESET_ALL + Style.BRIGHT)
                return WIN
            elif self.strikes == 8:
                print(Fore.BLACK + Back.RED + Style.DIM + "The platform falls out from underneath you and you die." + Style.RESET_ALL + Style.BRIGHT)
                return LOSE

            # Print the gameboard
            print("\n" + "   %s/8   " % self.strikes + Fore.RED + ''.join(['-' if self.usedletters[i] else chr(i+65) for i in range(26)]) + Fore.YELLOW)

            lines = getDrawing(self.strikes).split('\n')
            lines[3] += '    ' + Fore.MAGENTA + str(self.word) + Fore.YELLOW
            print('\n'.join(lines))

            time.sleep(0.5)
            # input
            a = None
            while(1):
                sys.stdout.write(Style.BRIGHT + Fore.CYAN + "Choose a letter, * to guess, or & to quit: ")
                sys.stdout.flush()
                c = getch.getch()
                a = ''
                if type(c) == type(a):  # Case: Unix
                    a = c.upper()
                else:  # Case: Windows
                    a = c.decode("UTF-8").upper()

                if re.match(r'[\w]', a):
                    if self.usedletters[ord(a) - 65]:
                        print("You already used that!")
                        continue
                    else:
                        sys.stdout.write(a)  # echo the letter
                        break
                elif a == '&':  # Quit
                    return QUIT  # exits play() method
                elif a == '*':
                    self.guessWord()
                    a = None  # so that it doesn't print Nope
                    break  # will loop back to the gameover check
                elif a == chr(3):
                    raise KeyboardInterrupt
                print("Not a valid letter")

            # end input loop
            if a is not None:
                sys.stdout.write('\n')
                ind = ord(a)-65
                self.usedletters[ind] = True
                result = self.word.guess(a)
                if (result):
                    print(Fore.WHITE + Back.GREEN + "You got one!" + Style.RESET_ALL + Style.BRIGHT)
                else:
                    print(Fore.BLACK + Back.RED + Style.DIM + "Nope!" + Style.RESET_ALL + Style.BRIGHT)
                    self.strikes += 1
            # gameloop
        # end of play()

    def guessWord(self):
        print('\nWORD GUESS   \nPress Ctrl+C to abort   Press ENTER when done')
        pos = 0

        def advanceCursor():
            nonlocal pos
            if not pos >= len(self.word) - 1:
                pos += 1
                # skip spaces
                while not pos >= len(self.word) - 1 and (self.word.answer[pos] == ' '):
                    pos += 1

        def backtrackCursor():
            nonlocal pos
            if not pos == 0:
                pos -= 1
                while not pos == 0 and self.word.answer[pos] == ' ':
                    pos -= 1

        guess = word.Word('')
        guess.answer = list(self.word.answer)
        guess.guessed = self.word.guessed
        while (1):
            sys.stdout.write('\r' + str(guess) + '\r')
            sys.stdout.write(word.Word.__str__(guess)[:pos*2])  # move cursor
            sys.stdout.flush()
            try:
                c = getch.getch()
            except KeyboardInterrupt:
                print('\nWord guess aborted')
                return CANCEL
            if ord(c) == 27:  # Arrow keys: Unix
                if ord(getch.getch()) == 91:
                    c = getch.getch()
                    if c == 'C':  # right arrow
                        advanceCursor()
                    elif c == 'D':  # left arrow
                        backtrackCursor()
            elif ord(c) == 224:  # Arrow keys: Windows
                c = getch.getch()  # 75 left 77 right
                if ord(c) == 75:
                    backtrackCursor()
                elif ord(c) == 77:
                    advanceCursor()
            elif ord(c) == 3 or c == '&':  # 3 = Ctrl - C
                print('\nWord guess aborted')
                return CANCEL
            elif ord(c) == 8 or c == ' ':  # Backspace (Ctrl - H)
                guess.guessed[pos] = False
            elif ord(c) == 13 or ord(c) == 10 or c == '\n':  # Newline and carriage return (enter)
                for i in guess.guessed:
                    if not i:
                        break
                else:
                    sys.stdout.write('\nPlease wait, checking your guess..')
                    sys.stdout.flush()
                    self.word.longGuess(str(guess.answer))
                    for i in range(len(self.word)):
                        time.sleep(.1)
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    return QUIT
            else:
                if type(c) == bytes:  # This happens on Windows
                    c = c.decode("utf-8")
                c = c.upper()
                if self.set.letterInSet(c):
                    guess.answer[pos] = c
                    guess.guessed[pos] = True
                    advanceCursor()
        # end of guessWord

    def playAgain(self, result):
        if result == WIN:
            print(Style.BRIGHT + "\nGame over!")
            print("The word was: " + Fore.RED + self.word.answer)
            print(Fore.CYAN + "Great job! You won!")
        elif result == LOSE:
            print(Style.BRIGHT + "\nGame over!")
            print("The word was: " + Fore.RED + self.word.answer)
            print(Fore.MAGENTA + "Seems like that was a pretty good word!")
        elif result == QUIT:
            print(Style.RESET_ALL + "\nGoodbye!")
            raise SystemExit
        elif result == CANCEL:
            print("Game cancelled.")
        else:
            print("Unknown exit condition! This is a bug!")
        sys.stdout.write(Style.RESET_ALL + Back.WHITE + Fore.BLACK + "Want to play again? (" + Fore.GREEN + "Y" + Fore.BLACK + "/" + Fore.RED + "n" + Fore.BLACK + ")" + Style.RESET_ALL + ' ')
        sys.stdout.flush()
        i = input()
        # first letter of 'no' and 'quit'
        if i[0] in 'NnQq':
            return False
        return True

if __name__ == "__main__":
    g = HangmanGame()
    while(g.playAgain(g.play())):
        g = HangmanGame()
    raise SystemExit
