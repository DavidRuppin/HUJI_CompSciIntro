#################################################################
# FILE : game_objects.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex10 2022-2023
#################################################################
import abc
from typing import NamedTuple, List, Union


class Location(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Location(self.row + other.row, self.col + other.col)

    def __eq__(self, other):
        try:
            return self.row == other[0] and self.col == other[1]
        except:
            return False

    def __gt__(self, other):
        return self.row > other.row or self.col > other.col

    def __lt__(self, other):
        return self.row < other.row or self.col < other.col



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


class Snake(HasGetLocations, DirectionalObject):
    DIRECTION_TO_RIGHT_ROTATE_DIRECTION = {Location(0, -1): Location(1, 0),
                                           Location(0, 1): Location(-1, 0),
                                           Location(-1, 0): Location(0, -1),
                                           Location(1, 0): Location(0, 1)}

    def __init__(self, location: Location, direction: Location = Location(1, 0)):
        self._head = location
        self._bod: List[Location] = []
        self.set_direction(direction)

    def set_direction(self, direction: Location):
        """
        @param direction: A directional vector
        """
        self._dir = direction

    def get_direction(self) -> Location:
        return self._dir

    def rotate_right(self):
        """
        Rotates the snake's direction 90 degrees to the right
        @return:
        """
        self.set_direction(Snake.DIRECTION_TO_RIGHT_ROTATE_DIRECTION[self.get_direction()])

    def rotate_left(self):
        """
        Rotates the snake's head 90 degrees to the left
        @return:
        """
        for _ in range(3):
            self.rotate_right()


    def move(self, do_pop: bool = True) -> Union[Location, None]:
        """Moves the snake in its current direction
        :@param do_pop: The flag that controls the removal of the last object of the snake
        :@return: the Location of the popped part of the snake if the body is not empty, None if it doesn't or if do_pop
                                        is set to False
        """
        self._bod.append(self.get_head_location())
        self._head += self.get_direction()
        if do_pop:
            return self.pop()


    def get_head_location(self) -> Location:
        return self._head

    def get_locations(self) -> List[Location]:
        return self._bod

    def get_entire_snake(self) -> List[Location]:
        return [self.get_head_location(), *self.get_locations()]

    def pop(self) -> Union[Location, None]:
        """
        Pops the FIRST element from the body, i.e. the last "part" of the snake
        @return: Location if the snake has a body, None otherwise
        """
        if len(self._bod):
            return self._bod.pop(0)
        return None

    def extend_rear(self, location: Location):
        """
        Adds the given location to the REAR of the snake, not the head
        @param location: The location to append
        @raise ValueError if the location is part of the snake already
        """
        if location not in self._bod:
            self._bod = [location] + self._bod
        else:
            raise ValueError(f'The location {location} exists already!')

class Apple(HasGetLocations):
    def __init__(self, location: Location):
        self._head = location

    def get_head_location(self) -> Location:
        return self._head

    def get_locations(self) -> List[Location]:
        return [self.get_head_location()]

class ScoreTracker:
    def __init__(self, score=0):
        self.score = score

    def get_score(self) -> int:
        return self.score

    def increase_score(self, amount: int):
        self.score += amount

    @staticmethod
    def get_score_increment(snake_size: int) -> int:
        """Calculates the amount the score should grow in a single turn for a given snake size"""
        return int(snake_size ** 0.5)