from typing import List

VERTICAL = 0
HORIZONTAL = 1


class Car:
    """
    Add class description here
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # implement your code and erase the "pass"
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self) -> List:
        """
        :return: A list of coordinates the car is in
        """
        # implement your code and erase the "pass"
        return [(self.location[0] + i, self.location[1]) if self.orientation == VERTICAL else (
            self.location[0], self.location[1] + i) for i in range(self.length)]

    def possible_moves(self) -> dict:
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        return {'u': 'up', 'd': 'down'} if self.orientation == VERTICAL else {'l': 'left', 'r': 'right'}

    def movement_requirements(self, move_key) -> List:
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        move_key_dict = {'u': -1, 'd': 1, 'l': -1, 'r': 1}
        row, col = self.car_coordinates()[-1 if move_key in ['d', 'r'] else 0]
        move = move_key_dict[move_key]
        return [(row + move, col) if self.orientation == VERTICAL else (row, col + move)]

    def move(self, move_key) -> bool:
        """ 
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        move_key_dict = {'u': -1, 'd': 1, 'l': -1, 'r': 1}
        if move_key in self.possible_moves():
            move = move_key_dict[move_key]
            row, col = self.location
            self.location = (row + move, col) if self.orientation == VERTICAL else (row, col + move)
            return True
        return False

    def get_name(self) -> str:
        """
        :return: The name of this car.
        """
        return self.name
