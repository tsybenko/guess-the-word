import termcolor


def warn(text):
    print(termcolor.colored(text, 'yellow'))


def success(text):
    print(termcolor.colored(text, 'green'))


def error(text):
    print(termcolor.colored(text, 'red'))
