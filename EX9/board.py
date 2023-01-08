from typing import List, Tuple, Union, Dict

# BOARD CONSTANTS #
BOARD_WIDTH, BOARD_HEIGHT = 7, 7

EMPTY_CELL = None
BLOCKED_CELL = '*'

EXIT_CELL = 'E'


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # implement your code and erase the "pass"
        self.arr = [[EMPTY_CELL for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.cars: Dict = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        new_board = [['*' for col in self.arr[0]] + ['|'] if row != self.target_location()[0] else
                     ['*' for col in self.arr[0]] + ['E'] for row in range(len(self.arr))]
        for car in self.cars:
            for cell in self.cars.get(car).car_coordinates():
                new_board[cell[0]][cell[1]] = car

        return '\n'.join([str(row) for row in new_board])

    def cell_list(self) -> List[Tuple]:
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        return [(row, col) for row in range(BOARD_HEIGHT) for col in range(BOARD_WIDTH)] + [self.target_location()]

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        # implement your code and erase the "pass"
        moves = []
        for car in self.cars.values():
            for move in car.possible_moves():
                if self.is_move_legal(move, car):
                    moves.append((car.get_name(), move, car.possible_moves().get(move, 'Gottem')))

        return moves

    def is_move_legal(self, move_key: str, car) -> bool:
        if move_key not in car.possible_moves():
            return False

        for cell in car.movement_requirements(move_key):
            if not self.is_cell_legal_and_empty(cell):
                return False

        return True

    def is_cell_legal_and_empty(self, cell: Tuple):
        return self.is_cell_in_bounds(cell) and self.cell_content(cell) is None

    def is_cell_in_bounds(self, cell: Tuple) -> bool:
        return cell in self.cell_list()

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return (3, 7)

    def cell_content(self, coordinate) -> Union[str, None]:
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        for car in self.cars.values():
            if coordinate in car.car_coordinates():
                return car.get_name()

        return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        for name in self.cars:
            if car.get_name() == name:
                return False

        for cell in car.car_coordinates():
            if not self.is_cell_legal_and_empty(cell):
                return False

        self.cars[car.get_name()] = car
        return True

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name in self.cars and self.is_move_legal(move_key, self.cars.get(name)):
            return self.cars.get(name).move(move_key)

        return False
