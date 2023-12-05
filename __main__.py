from sutom.game import Sutom

def main():
    game: Sutom = Sutom(attemptLimit=10)

    # Loop until the game is over.
    while game.run():
        continue


main()