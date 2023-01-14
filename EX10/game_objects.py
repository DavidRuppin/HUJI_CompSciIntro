#################################################################
# FILE : game_objects.py
# WRITER 1: David Ruppin, ruppin, 322296336
# WRITER 2: Shachar Cohen, 206532418
# EXERCISE : intro2cs ex10 2022-2023
#################################################################

'''DESCRIPTION: game_objects.py module contains the classes for the objects in the game.
             Objects included here:
              1. Snake
              2. Apple
              3. Score Tracker
              4. Location (inner attribute of the objects in the game)
              5. HasGetLocations (checks if an object has location)'''

#######################   IMPORTS   ##############################
from game_utils import get_random_wall_data
from typing import List, Union
from interfaces import *


#################################################################

class Snake(HasGetLocations, DirectionalObject):
    DIRECTION_TO_RIGHT_ROTATE_DIRECTION = {Location(0, -1): Location(1, 0),
                                           Location(0, 1): Location(-1, 0),
                                           Location(-1, 0): Location(0, -1),
                                           Location(1, 0): Location(0, 1)}

    def __init__(self, head: Location, direction: Location = Location(1, 0)):
        self._head = head
        self._bod: List[Location] = [head + direction * -2, head + direction * -1]
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
        :@return: the Location of the popped part of the snake if the body is not empty,
                     None if it doesn't or if do_pop is set to False
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

    def snip_body(self, location: Location):
        """Attempts to cut the body from @location and down"""
        while self.pop() != location:
            continue


class RoundManager:
    def __init__(self, rounds: int):
        """
        @param rounds: The number of rounds that should be played, -1 for infinite
        """
        self.rounds = rounds + 1 if rounds >= 0 else rounds

    def finish_round(self):
        """Decreases the round counter if rounds is not 0 or -1"""
        if self.rounds > 0:
            self.rounds -= 1

    def is_game_over(self) -> bool:
        return self.rounds == 0

    def finish_game(self):
        self.rounds = 0


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


class Wall(HasGetLocations, DirectionalObject):
    SIZE = 3
    COLOR = "Blue"

    def __init__(self) -> None:
        x, y, dir = get_random_wall_data()
        self._dir = dir
        self._locations: List[Location] = self.init_locations(y, x)
        self._head = self.init_head()

    def init_locations(self, row: int, col: int) -> List[Location]:
        '''inits the location of the wall according to its direction.
        for vertical direction - the locations will be vertical (same col).
        for horizontal direction - the locations will be horizontal.
        @return: lists of 3 locations.'''
        LOCATION_BY_DIRECTION = {"Up": [Location(row + i, col) for i in range(-1, 2)], \
                                 "Down": [Location(row + i, col) for i in range(-1, 2)], \
                                 "Left": [Location(row, col + i) for i in range(-1, 2)], \
                                 "Right": [Location(row, col + i) for i in range(-1, 2)]}
        return LOCATION_BY_DIRECTION[self.get_direction()]

    def get_locations(self) -> List[Location]:
        return self._locations

    def get_direction(self) -> Location:
        return self._dir

    def init_head(self) -> Location:
        # If we're headed up or to the left then the head is the 'first' location of the snake, otherwise it's the last
        HEAD_BY_DIRECTION = {"Up": self.get_locations()[0], \
                             "Down": self.get_locations()[-1], \
                             "Left": self.get_locations()[0], \
                             "Right": self.get_locations()[-1]}
        return HEAD_BY_DIRECTION[self.get_direction()]

    def get_head_location(self) -> Location:
        return self._head

    def move(self) -> bool:
        MOVE_BY_DIRECTION = {"Up": (-1, 0), "Down": (1, 0), "Right": (0, 1), "Left": (0, -1)}
        self._locations = [loc + MOVE_BY_DIRECTION[self.get_direction()] for loc in self._locations]
        self._head += MOVE_BY_DIRECTION[self.get_direction()]
