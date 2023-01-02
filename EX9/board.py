from collections import defaultdict
from typing import Optional, Tuple, List, Set, Union

from car import Car
from car import Location

# BOARD CONSTANTS #
BOARD_WIDTH, BOARD_HEIGHT = 7, 7

EMPTY_CELL = None
BLOCKED_CELL = '*'

EXIT_LOCATION = Location(3, 7)
EXIT_CELL = 'E'


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        self._board_array: List[List[Optional[str, None]]] = Board.init_board()
        self._cars: dict[str, Optional[Car, None]] = defaultdict(lambda: None)


    @staticmethod
    def init_board():
        board = [[EMPTY_CELL] * BOARD_WIDTH for row in range(BOARD_HEIGHT)]

        # Adding the blocked cells at the end and the exit
        for row in range(BOARD_HEIGHT):
            if row == EXIT_LOCATION[0]:
                board[row].append(EXIT_CELL)
            else:
                board[row].append(BLOCKED_CELL)

        return board

    def __str__(self) -> str:
        board = Board.init_board()
        for car in self.get_cars():
            for loc in car.get_locations():
                board[loc.row][loc.col] = car.get_name()

        return str(board).replace('], [', '],\n[')

    def __repr__(self) -> str:
        return str(self)

    def cell_list(self) -> List[Location]:
        """
        Iterating over the board's size, appending the coordinates one by one to a list, then adding the exit
        and returning the list
        @return:
        """
        cells = []
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                cells.append(Location(row, col))

        cells.append(EXIT_LOCATION)

        return cells

    def possible_moves(self) -> List[Tuple[str]]:
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]

        moves = []
        for car in self.get_cars():
            name = car.get_name()
            curr_moves = car.possible_moves()
            for move in curr_moves:
                # If we can move the car to the given location, append that move
                if self.move_car(name, move):
                    moves.append((name, move, curr_moves[move]))
                    self.pop_car(name)
                    self.add_car(car)

        return moves

    def target_location(self) -> Location:
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return EXIT_LOCATION

    def cell_content(self, coordinate: Tuple[int, int]) -> Union[Car, None]:
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        row, col = coordinate
        if self._board_array[row][col] == BLOCKED_CELL:
            return None

        for car in self.get_cars():
            for location in car.get_locations():
                if (row, col) == location:
                    return car.get_name()

        return None

    def get_cars(self) -> List[Car]:
        # Filtering None values if any exist
        return list(filter(lambda car: car is not None, self._cars.values()))

    def get_car_names(self) -> List[str]:
        return list(self._cars)

    def add_car(self, car) -> bool:
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """

        if type(car) is Car and self.is_car_addable(car):
            self._cars[car.get_name()] = car
            return True

        return False

    def pop_car(self, name) -> Union[Car, None]:
        """
        Attempts to remove a car by name, returning the Car object on success
        @param name: The name of the car to be removed
        @return: the Car object on success, None if it doesn't exist
        """
        if self._cars[name] is not None:
            return self._cars.pop(name)
        return None

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        car = self.pop_car(name)

        # If the car exists on the board and the move is legal
        if car is not None:
            if  move_key in car.possible_moves():
                _, length, location, orientation = car.get_init_params()

                # Creating a new car with the starting location altered according to the move
                new_car = Car(name,
                              length,
                              location  + Car.MOVEMENT_GEOMETRIC_MEANING[move_key],
                              orientation)


                # If the new car can be added, add it and return True
                # Otherwise the car cannot move in the requested direction and the original car is added back to the board
                if (self.add_car(new_car)):
                    return True

            self.add_car(car)
        return False

    def is_car_addable(self, car: Car) -> bool:
        """
        Checking if @car can be placed in the board
        @param car: The Car to place
        @return: True if the car can be placed, False if it can't
        """

        # Checking whether the name exists already
        if not self._cars.get(car.get_name()) is None:
            return False

        car_locs: Set[Location] = car.get_locations()

        # Checking if the car is out of bounds
        for loc in car_locs:
            if not self.is_location_in_board(loc):
                return False

        # Checking whether any existing car intersects with the new car
        for existing_car in self.get_cars():
            if existing_car.get_locations().intersection(car_locs):
                return False

        return True

    def is_location_in_board(self, loc: Location) -> bool:
        """
        Checks if a location is within the boundaries of the board, regardless of any other rules
        @param loc: The Location to check
        @return: True if the location is within the board, False if not
        """
        return (loc.row in range(7) and loc.col in range(7)) or loc == EXIT_LOCATION



if __name__ == '__main__':
    # TODO - Delete us
    from board import Board
    from car import Car
    from pprint import pprint as pp
    b = Board()
    car = Car('David', 8, (3, 0), 1)
    car2 = Car('Bavid', 1, (3, 7), 1)
    b.add_car(car)
    b.add_car(car2)
    b.move_car('f', 'u')
    print(b)
    f = b.cell_content(EXIT_LOCATION)
    f