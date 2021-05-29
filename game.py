import art
import json
import math
import os
import prettytable
import random
import terminal
import termcolor

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
WORDS_FILE_PATH = os.path.join(DATA_PATH, 'words.json')
SCOREBOARD_FILE_PATH = os.path.join(DATA_PATH, 'scoreboard.json')


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

    def get_data(self, file_path):
        json_decoder = json.decoder.JSONDecoder()

        with open(file_path, 'r') as file:
            file_data = file.read()

            if len(file_data) == 0:
                file_data = '[]'

            results: list = json_decoder.decode(file_data)

        file.close()
        return results

    def get_amount(self):
        return self._amount

    def add(self, amount):
        self._amount += amount

    def get_table(self):
        table = prettytable.PrettyTable()
        table.add_column('Total Score', str(self._amount))
        return table.get_string()


class Player:
    def __init__(self, nickname):
        self.scoreboard = Scoreboard()
        self.nickname = nickname

    def save_score(self, amount):
        def write_data(file_path, data):
            with open(file_path, 'w') as file:
                file.write(data)
            file.close()

        def clear_file(file_path):
            with open(file_path, 'w') as file:
                pass
            file.close()

        results = self.scoreboard.get_data(SCOREBOARD_FILE_PATH)

        player = None

        for record in results:
            if record['nickname'] == self.nickname:
                record["score"] = amount
                player = record

        if player is None:
            results.append({
                'nickname': self.nickname,
                'score': amount
            })

        clear_file(SCOREBOARD_FILE_PATH)
        write_data(SCOREBOARD_FILE_PATH, json.dumps(results))


class GameSession:
    IS_RUNNING = False

    def __init__(self, player):
        self.player = player
        self.scoreboard = Scoreboard()
        self.table = prettytable.PrettyTable()

    def _show_leaders(self):
        table = prettytable.PrettyTable()
        table.field_names = ['Nickname', 'Score']
        players = self.player.scoreboard.get_data(SCOREBOARD_FILE_PATH)
        for player in sorted(players, key=lambda player: player['score'], reverse=True):
            table.add_row([player["nickname"], player["score"]])
        print('\n==== Leaderboard ====\n')
        print(table.get_string())

    def _start_loop(self):
        repeat = True
        while self.IS_RUNNING:
            self.word = get_random_word()
            self.attempted_letters = []
            self.display = ['_' for _ in self.word]
            self.attempts_available = math.ceil(len(self.word) / 2)
            self.guessed_letters = []
            self.not_guessed_letters = []

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
                    self.scoreboard.add(50)
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

                self.player.save_score(self.scoreboard.get_amount())

            self.IS_RUNNING = input('\nWant to play again? [Y/N]\n').lower() == 'y'

    def _print_results(self):
        print(self.scoreboard.get_table())

    def run(self):
        art.tprint('Guess The Word')

        self.IS_RUNNING = True
        self._start_loop()
        self._print_results()
        self._show_leaders()
