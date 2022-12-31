from typing import List

from EX9.board import Board
from EX9.car import Car
from EX9.helper import load_json, Location

LEGAL_CAR_NAMES = ['Y','B','O','G','W','R']

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
        # implement your code and erase the "pass"
        while self._board.cell_content(self._board.target_location()) is None:



    @staticmethod
    def get_cars_from_json(filename: str) -> List[Car]:
        """

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






if __name__== "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    # implement your code and erase the "pass"
    # TODO - Implement the command line input handler and deal with empty / problematic json paths
    print(Game.get_cars_from_json('car_config.json'))
