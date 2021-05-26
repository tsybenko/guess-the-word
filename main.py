import math
import random
import art

app_name = 'Guess The Word'

words = [
    "python",
    "marquee",
    "apple",
    "programming"
]


def get_header():
    return art.text2art(app_name)


def start_game():
    print(get_header())

    word = random.choice(words)
    display = ['_' for _ in word]
    attempts = math.ceil(len(word) / 2)

    # print(f'The word is - {word}')

    while attempts > 0:
        if ''.join(display) == word:
            break

        print(f'Attempts: {attempts}')
        print(''.join(display))

        guess_letter = input('Guess a letter: ').lower()

        if guess_letter in word:
            for pos in range(len(word)):
                letter = word[pos]

                if guess_letter == letter:
                    display[pos] = letter
        else:
            attempts -= 1

    return 0


if __name__ == '__main__':
    start_game()
