#################################################################
# FILE : game_objects.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex11 2022-2023
#################################################################
from typing import NamedTuple
from typing import List, Iterable, Optional

class Location(NamedTuple):
    row: int
    col: int

    def __eq__(self, other):
        if type(other) is Location:
            return self.row == other.row and self.col == other.col
        else:
            return (self.row, self.col) == other


BoardType = List[List[str]]
Path = List[Location]


class Board:
    def __init__(self, board: BoardType):
        self._board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_location_neighbors(self, location: Location):
        neighbors = []

        row, col = location
        # Iterating over the 3x3 square of locations where @location is its center
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_loc = Location(row + i, col + j)
                # Checking whether the new location is out of bounds or is the original location
                if not self.is_location_in_board(new_loc) or new_loc == location:
                    continue
                neighbors.append(new_loc)

        return neighbors

    def is_location_in_board(self, location: Location) -> bool:
        """

        @param location: The location to check
        @return: True if @location is in the board, False otherwise
        """
        row, col = location
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return True

    def are_neighbors(self, loc1: Location, loc2: Location) -> bool:
        return abs(loc1.row - loc2.row) <= 1 and abs(loc1.col - loc2.col) <= 1

    def is_path_valid(self, path: Path, words: Iterable[str]) -> Optional[str]:
        """Checks if a path doesn't repeat two Locations and if the word it makes is in the words iterable"""
        word = self.word_from_locations(path)
        unique_path = set(path)
        # checks to see if the origin path had duplicate locations
        if len(path) != len(unique_path):
            return None

        return word if word in words else None

    def get_location(self, location: Location) -> str:
        row, col = location
        return self._board[row][col]

    def word_from_locations(self, locations: Path) -> Optional[str]:
        return ''.join(self.get_location(location) for location in locations)
