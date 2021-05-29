import game

if __name__ == '__main__':
    nickname = ''

    while nickname == '':
        nickname = input('Enter your nickname: ')

    player = game.Player(nickname)
    game = game.GameSession(player)
    game.run()
