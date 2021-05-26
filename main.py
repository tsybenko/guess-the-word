import math
import random
import art
import json
import termcolor

app_name = 'Guess The Word'


def get_header():
    return art.text2art(app_name)


def get_words():
    with open('words.json', 'r') as file:
        json_data = json.load(file)

    return json_data


def start_game():
    is_running = True
    words = get_words()

    print(get_header())

    word = random.choice(words)
    attempted_letters = []
    display = ['_' for _ in word]
    attempts = math.ceil(len(word) / 2)

    # print(f'The word is - {word}')

    while is_running:
        if ''.join(display) == word:
            print(f'It\'s "{word}"')
            print(termcolor.colored('You win!', 'green'))
            break

        if attempts < 1:
            print(termcolor.colored('Game over!', 'red'))
            print(f'The word was - "{word}"')
            break

        print(f'Attempts: {attempts}')
        print(''.join(display))

        if len(attempted_letters) > 0:
            print('Letters attempted: ' + ', '.join(attempted_letters))

        input_letter = input('Guess a letter: ').lower()

        letter_guessed = False
        if input_letter in word:
            for pos in range(len(word)):
                letter = word[pos]

                if input_letter == letter:
                    letter_guessed = True
                    display[pos] = letter
        else:
            attempts -= 1

        colored_letter = termcolor.colored(input_letter, 'green' if letter_guessed else 'red')
        if colored_letter not in attempted_letters:
            attempted_letters.append(colored_letter)

    return 0


if __name__ == '__main__':
    start_game()
