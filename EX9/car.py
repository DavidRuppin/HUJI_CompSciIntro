from typing import Tuple, Dict, List
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

    MOVEMENT_MESSAGES_HORIZONTAL = { 'l': 'The car will side-jump to the left',
                                    'r': 'The car will now support Ben Gvir' }

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
        self._location = location
        self._orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        # implement your code and erase the "pass"
        row, col = self._location
        return [(row + i, col) if self._orientation == Car.VERTICAL else (row, col + i) for i in range(self._length)]


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

    def get_locations(self) -> List[Location]:
        """
        @return: A list of the car's Location objects with the location of this car as the head and the car's size
        as the size
        """
        locations = []

        row, col = self._location

        for i in range(self._length):
            # If the orientation is vertical then 1 - orientation == 1 and the rows will decrease and the cols will not
            # otherwise the cols will increase and the rows won't change
            location = Location(row + i * (1 - self._orientation), col + i * (self._orientation))
            locations.append(location)

        return locations
