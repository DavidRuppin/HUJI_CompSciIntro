from typing import Tuple, Dict, List, Set
from helper import Location


class Car:
    """
    Add class description here
    """

    # CAR CONSTANTS #
    VERTICAL = 0
    HORIZONTAL = 1

    MOVEMENT_MESSAGES_VERTICAL = {'u': 'The car will be teleported up one cell',
                                  'd': 'The car will be smashed so bad it\'ll descend one cell'}

    MOVEMENT_MESSAGES_HORIZONTAL = {'l': 'The car will side-jump to the left',
                                    'r': 'The car will now support Ben Gvir'}

    MOVEMENT_GEOMETRIC_MEANING = {'u': Location(-1, 0), 'd': Location(1, 0),
                                  'l': Location(0, -1), 'r': Location(0, 1)}

    def __init__(self, name: str, length: int, location: Tuple[int, int], orientation: int):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # implement your code and erase the "pass"
        self._name = name
        self._length = length
        self._location: Location = Location(*location)
        self._orientation = orientation

    def car_coordinates(self) -> List[Location]:
        """
        :return: A list of coordinates the car is in
        """
        return list(self.get_locations())

    def possible_moves(self) -> Dict[str, str]:
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        return Car.MOVEMENT_MESSAGES_VERTICAL if self._orientation == Car.VERTICAL else Car.MOVEMENT_MESSAGES_HORIZONTAL

    def movement_requirements(self, move_key) -> List[Tuple]:
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal or an empty list
                                                                                                if the move is illegal
        """
        if move_key not in self.possible_moves():
            return []

        row, col = self._location
        if move_key == 'u':
            return [(row - 1, col)]
        elif move_key == 'd':
            return [(row + 1, col)]
        elif move_key == 'l':
            return [(row, (col - 1))]
        elif move_key == 'r':
            return [(row, (col + 1))]

    def move(self, move_key) -> bool:
        """ 
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        return True if move_key in self.possible_moves() else False

    def get_name(self) -> str:
        """
        :return: The name of this car.
        """
        return self._name

    def get_locations(self) -> Set[Location]:
        """
        @return: A set of the car's Location objects with the location of this car as the head and the car's size
        as the size
        """

        row, col = self._location

        locations = {Location(row + i, col) if self._orientation == Car.VERTICAL else Location(row, col + i) for
                     i in range(self._length)}

        return locations

    def get_init_params(self) -> Tuple[str, int, Location, int]:
        """
        A function to easily replicate the car and alter its creation parameters
        @return: All the __init__ parameters
        """
        return (self.get_name(), self._length, self._location, self._orientation)