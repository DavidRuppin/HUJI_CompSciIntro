#################################################################
# FILE : snake_main.py
# WRITER 1: David Ruppin, ruppin, 322296336
# WRITER 2: Shachar Cohen, 206532418
# EXERCISE : intro2cs ex10 2022-2023
#################################################################
'''DESCRIPTION: snake_main.py contains the main loop for the game. 
                main loop function runs the game using SnakeGame object from 
                snake_game module (with given args parameters) and controls the visual display
                of the game using GameDisplay object from game_display module'''
#######################   IMPORTS   #############################
import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay
#################################################################

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    # INIT OBJECTS
    game = SnakeGame(args)
    gd.show_score(0)
    # DRAW BOARD
    game.draw_board(gd)
    # END OF ROUND 0
    while not game.is_over():
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects()
        score = game.get_score()
        gd.show_score(score)
        # DRAW BOARD
        game.draw_board(gd)
        # WAIT FOR NEXT ROUND:
        game.end_round()
        try:
            gd.end_round()
        except ValueError:
            game.finish_game()

    try:
        game.draw_board(gd)
    except:
        # TODO - Consider changing this
        pass

    # FIXME - Delete
    # from time import sleep
    # sleep(3000)

if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")
    # from game_display import setup_game
    # gd = setup_game(argparse.Namespace(width=40, height=30, apples=0, debug=False, walls=0, rounds=-1, seed=None, verbose=False, delay=100))
    # gd.start()
