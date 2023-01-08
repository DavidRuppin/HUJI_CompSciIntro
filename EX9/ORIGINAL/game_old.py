import re
import sys
from typing import List

from board import Board
from car import Car
from helper import load_json

LEGAL_CAR_NAMES = ['Y','B','O','G','W','R']
LEGAL_MOVES = ['u', 'd', 'l', 'r']

GAME_END_MESSAGE = "{} has reached the target location, the game is OVER! Good job m8"
class Game:
    """
    Add class description here
    """

    def __init__(self, board: Board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code and erase the "pass"
        self._board: Board = board
        self._move_validity_regex = Game.create_command_regex_verifier(board.get_car_names(), LEGAL_MOVES)

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        # implement your code and erase the "pass"
        pass

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """


        while self._board.cell_content(self._board.target_location()) is None:
            print(self._board)
            inp = input("Enter your move: ")

            # If the user wants to quit, let him
            if inp.strip() == '!':
                return

            if re.fullmatch(self._move_validity_regex, inp):
                name, move = inp.split(',')
                if self._board.move_car(name, move):
                    print("Great success!")
                else:
                    print("Couldn't perform '{},{}'".format(name, move))
            else:
                print('Bad input buddy, the valid commands are {} and the format is NAME,COMMAND'.format(LEGAL_MOVES))

        print(self._board)
        print(GAME_END_MESSAGE.format(self._board.cell_content(self._board.target_location())))



    @staticmethod
    def get_cars_from_json(filename: str) -> List[Car]:
        """
        Loads all the LEGITIMATE cars from a given file
        @param filename: The JSON to load
        @return: A list of cars (could be empty)
        """
        contents = load_json(filename)
        cars: List[Car] = []

        for name in contents:
            if name in LEGAL_CAR_NAMES:
                car_params = contents[name]
                if Game.check_car_params(car_params):
                    cars.append(Car(name, *car_params))

        return cars

    @staticmethod
    def check_car_params(params):
        """
        Checking that all the parameters are valid and correct GAME WISE (not checking if they collide on the board,
                                                                            just types and basic rules)
        @param params:
        @return:
        """
        if type(params) != list or len(params) != 3 or type(params[1]) != list or len(params[1]) != 2:
            return False
        length, location, orientation = params

        if isinstance(length, int) and  2 <= length <= 4:
            if type(location[0]) == type(location[1]) == int:
                # Just a silly way to check if the orientation is 0 or 1 :P
                if orientation ** 2 == orientation:
                    return True

        return False

    @staticmethod
    def create_command_regex_verifier(car_names: List[str], legal_moves: List[str]):
        REG_FORMAT = '[{}]\,[{}]'
        return re.compile(REG_FORMAT.format(''.join(car_names), ''.join(legal_moves)))


if __name__== "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    # implement your code and erase the "pass"
    args = sys.argv
    if args and len(args) == 2:
        json_path = args[1]

        board = Board()
        for car in Game.get_cars_from_json(json_path):
            board.add_car(car)

        game = Game(board)
        game.play()
