import game

def main():

    while True:
        game.handle_inputs()

        game.update()

        game.render()

if __name__ == "__main__":
    main()