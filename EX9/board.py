from typing import Optional, Tuple

from EX9.car import Car

# BOARD CONSTANTS #
BOARD_WIDTH, BOARD_HEIGHT = 7, 7

EMPTY_CELL = None
BLOCKED_CELL = '*'

EXIT_LOCATION = (3, 7)
EXIT_CELL = 'E'

class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        self._board_array = [[EMPTY_CELL] * BOARD_WIDTH for row in range(BOARD_HEIGHT)]
        self._cars = []

        # Adding the blocked cells at the end and the exit
        for row in range(BOARD_HEIGHT):
            if row == EXIT_LOCATION[1]:
                self._board_array[row].append(EXIT_CELL)
            else:
                self._board_array[row].append(BLOCKED_CELL)


    def __str__(self) -> str:
        return str(self._board_array)


    def cell_list(self) -> list:
        """
        Iterating over the board's size, appending the coordinations one by one to a list, then adding the exit
        and returning the list
        @return:
        """
        cells = []
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                cells.append((row, col))

        cells.append(EXIT_LOCATION)

        return cells

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        # implement your code and erase the "pass"
        pass

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        # implement your code and erase the "pass"
        pass

    def cell_content(self, coordinate: Tuple[int, int]) -> Optional[Car, None]:
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        row, col = coordinate
        if self._board_array[row][col] != EMPTY_CELL:
            return False

        for car in self._cars:
            for location in car.get_locations():
                if (row, col) == location:
                    return False

        return True



    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        pass

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        pass
