#################################################################
# FILE : game_super_classes.py
# WRITER 1: David Ruppin, ruppin, 322296336
# WRITER 2: Shachar Cohen, 206532418
# EXERCISE : intro2cs ex10 2022-2023
#################################################################
#######################   IMPORTS   ##############################
import abc # provides the infrastructure for defining custom abstract base classes
from typing import NamedTuple, List, Union
#################################################################

class Location(NamedTuple):
    '''Location class is designed to be an inner object in each of the objects in the game.
    It simplifies changing the locations of the objects in the game.'''
    row: int # represented by y in this exercise
    col: int # represented by x in this exercise

    def __add__(self, other):
        ''' + operator with Location object is defined in this way:
        loc_1 + loc_2 = Location (loc_1.row + loc_2.row, loc_1.col + loc_2.col)'''
        if isinstance(other, Location):
            return Location(self.row + other.row, self.col + other.col)
        elif (isinstance(other, tuple) or isinstance(other, list))\
                and len(other) == 2:
            return Location(self.row + other[0], self.col + other[1])
        else:
            raise ValueError\
                ("Locations can only be added to Locations, tuples or lists of length 2")

    def __mul__(self, other: int):
        """

        @param other: A number
        @return:
        """
        return Location(self.row * other, self.col * other)


    def __eq__(self, other):
        ''' == operator with Location object is defined in this way:
        for Location objects - it compares rows and cols parameters.
        for lists and tuples of length 2 - checks if tuple[1] == row and tuple[0] == col
        for other instances - returns False'''
        if isinstance(other, Location):
            return self.row == other.row and self.col == other.col
        elif (isinstance(other, tuple) or isinstance(other, list))\
                and len(other) == 2:
            return self.row == other[0] and self.col == other[1]
        else:
            return False

    def __gt__(self, other):
        ''' > operator with Location object. Constructed similarly to == operator.'''
        if isinstance(other, Location):
            return self.row > other.row or self.col > other.col
        elif (isinstance(other, tuple) or isinstance(other, list))\
                and len(other) == 2:
            return self.row > other[0] or self.col > other[1]
        else:
            return False

    def __lt__(self, other):
        ''' < operator with Location object. Constructed similarly to == operator.'''
        if isinstance(other, Location):
            return self.row < other.row or self.col < other.col
        elif (isinstance(other, tuple) or isinstance(other, list))\
            and len(other) == 2:
            return self.row < other[0] or self.col < other[1]
        else:
            return False
    
    def intersection(self, other):
        intersection = set()
        if type(other) == list or type(other) == set:
            for item in other:
                if item == self:
                    return intersection.add(item)
            return intersection
        else:
            if self == other:
                return {other}
            else:
                return intersection


# Interfaces / Abstract Classes
class HasGetLocations(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_locations(self) -> List[Location]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_head_location(self) -> Location:
        raise NotImplementedError


class DirectionalObject(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_direction(self) -> Location:
        """Returns the direction as a Location object that can be added to the head to move the object
        practically a directional vector starting at (0, 0)"""
        raise NotImplementedError

    def move(self) -> bool:
        """Moves the object according to its direction"""
        raise NotImplementedError