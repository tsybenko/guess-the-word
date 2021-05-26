import math
import random
import art
import json
import termcolor
import terminal

alphabet = [
    'a', 'b', 'c', 'd',
    'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p',
    'q', 'r', 's', 't',
    'u', 'v', 'w', 'x',
    'y', 'z'
]


def get_words():
    with open('words.json', 'r') as file:
        json_data = json.load(file)

    return json_data


def get_random_word():
    words = get_words()
    return random.choice(words)


def start_game(score):
    is_running = True
    is_win = False
    word = get_random_word()
    attempted_letters = []
    display = ['_' for _ in word]
    attempts_available = math.ceil(len(word) / 2)

    # print(f'The word is - {word}')

    while is_running:
        if ''.join(display) == word:
            print(f'\nIt\'s "{word}"')
            terminal.success('You win!')
            is_win = True
            break

        if attempts_available < 1:
            terminal.error('Game over!')
            print(f'It was "{word}" word')
            break

        print(f'Attempts remaining: {attempts_available}')
        print(''.join(display))

        if len(attempted_letters) > 0:
            print('Letters attempted: ' + ', '.join(attempted_letters))

        input_letter = input('Guess a letter: ').lower()

        # if input_letter == word:
        #     score += 50
        #     terminal.success('BINGO!')
        #     break

        if len(input_letter) > 1:
            terminal.warn('Only 1 letter could be passed')
            continue
        elif input_letter not in alphabet:
            terminal.warn('The value must be an alphabetical letter')
            continue

        letter_guessed = False
        if input_letter in word:
            for pos in range(len(word)):
                letter = word[pos]

                if input_letter == letter:
                    letter_guessed = True
                    display[pos] = letter
                    score += 1
        else:
            attempts_available -= 1

        colored_letter = termcolor.colored(input_letter, 'green' if letter_guessed else 'red')
        if colored_letter not in attempted_letters:
            attempted_letters.append(colored_letter)

    return {
        "is_win": is_win,
        "attempted_letters": len(attempted_letters),
        "bad_attempts": len(attempted_letters) - len(word),
        "score": score
    }


if __name__ == '__main__':
    art.tprint('Guess The Word')

    win_count = 0
    points = 0
    repeat = True
    while repeat:
        result = start_game(points)

        if result["is_win"]:
            win_count += 1
            points = result["score"]

        if win_count > 1:
            points *= 2

        answer = input('\nDo you want to retry? [Y/N]\n')
        repeat = True if answer.lower() == 'y' else False

    print(f'You have {points} points. Thank you for game!')
