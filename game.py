import art
import json
import math
import os
import prettytable
import random
import terminal
import termcolor


WORDS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/words.json')


def get_words():
    with open(WORDS_FILE_PATH) as file:
        json_data = json.load(file)

    return json_data


def get_random_word():
    words = get_words()
    return random.choice(words)


class Scoreboard:
    def __init__(self, amount=0):
        self._amount = amount

    def get_amount(self):
        return self._amount

    def add(self, amount):
        self._amount += amount

    def get_table(self):
        table = prettytable.PrettyTable()
        table.add_column('Total Score', str(self._amount))
        return table.get_string()


class GameSession:
    IS_RUNNING = False

    def __init__(self):
        self.scoreboard = Scoreboard()
        self.table = prettytable.PrettyTable()
        self.word = get_random_word()
        self.attempted_letters = []
        self.display = ['_' for _ in self.word]
        self.attempts_available = math.ceil(len(self.word) / 2)
        self.guessed_letters = []
        self.not_guessed_letters = []

    def _start_loop(self):
        repeat = True
        while self.IS_RUNNING:
            while repeat:
                guessed = ''.join(self.display)

                if self.attempts_available < 1:
                    terminal.error('\nGame over!\n')
                    print(f'It was "{self.word}" word')
                    break

                if guessed == self.word:
                    terminal.success('\nWell done! You win!\n')
                    break

                print('Guessed:', guessed, '\n')
                print('Attempts remaining:', self.attempts_available)

                if len(self.attempted_letters) > 0:
                    print('Letters attempted: ' + ', '.join(self.attempted_letters), '\n')

                input_letter = input('Enter a letter: ').lower()

                if not input_letter.isalpha():
                    terminal.warn(f'\nYou entered "{input_letter}". It\'s not alphabetical character!\n')
                    continue

                if len(input_letter) > 1:
                    terminal.warn('\nOnly 1 letter or full word could be passed\n')
                    continue

                if input_letter == self.word:
                    terminal.success('\nBingo! You Guessed!\n')
                    break

                letter_guessed = False
                if input_letter in self.word:
                    for pos in range(len(self.word)):
                        letter = self.word[pos]

                        if input_letter == letter:
                            letter_guessed = True
                            self.display[pos] = letter

                            if input_letter not in self.guessed_letters:
                                self.scoreboard.add(1)
                                self.guessed_letters.append(input_letter)
                else:
                    self.attempts_available -= 1
                    self.not_guessed_letters.append(input_letter)

                colored_letter = termcolor.colored(input_letter, 'green' if letter_guessed else 'red')
                if colored_letter not in self.attempted_letters:
                    self.attempted_letters.append(colored_letter)

                # self.attempted_letters = [terminal.success(letter) for letter in self.guessed_letters] + [terminal.error(letter) for letter in self.not_guessed_letters]
                # self.attempted_letters.sort()

                # print(self.guessed_letters, self.not_guessed_letters)

            self.IS_RUNNING = input('\nWant to play again? [Y/N]\n').lower() == 'y'

    def _print_results(self):
        print(self.scoreboard.get_table())

    def run(self):
        art.tprint('Guess The Word')

        self.IS_RUNNING = True
        self._start_loop()
        self._print_results()
