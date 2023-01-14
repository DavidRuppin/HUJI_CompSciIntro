from functools import lru_cache
from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = Tuple[int, int]


class BoardObject:
    def __init__(self, board: Board):
        self._board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_location_neighbors(self, location: Location):
        neighbors = []

        row, col = location
        # Iterating over the 3x3 square of locations where @location is its center
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_loc = (row + i, col + j)
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
        row_index1, col_index1 = loc1
        row_index2, col_index2 = loc2
        if abs(row_index1 - row_index2) <= 1 and abs(col_index1 - col_index2) <= 1:
            return True
        return False

    def is_path_valid(self, path: Path, words: Iterable[str]) -> Optional[str]:
        word = ''
        path_length = len(path)
        unique_path = set(path)
        # checks to see if the origin path had duplicate locations
        if len(path) != len(unique_path):
            return None
        # Iterating over the locations in the given path
        for loc_index in range(path_length):
            # Making sure the location is in the board
            if not self.is_location_in_board(path[loc_index]):
                return None
            # And that two
            elif loc_index < path_length - 1:
                if not self.are_neighbors(path[loc_index], path[loc_index + 1]):
                    return None
            loc_row, loc_col = path[loc_index]
            word += self.get_location((loc_row, loc_col))
            if word in words:
                return word
        return None

    def get_location(self, location: Location) -> str:
        row, col = location
        return self._board[row][col]


def get_n_sized_paths_from_location(board: BoardObject, locations: Path, words: Iterable[str], count,
                                    paths: List[Path]) -> List[Path]:
    # Get all the paths from the last location in the @locations list [which is the tail of the current path]
    if count == 1:
        if board.is_path_valid(locations, words):
            paths.append([*locations])
        return

    for neighbor in board.get_location_neighbors(locations[-1]):
        if neighbor in locations:
            continue

        locations.append(neighbor)
        get_n_sized_paths_from_location(board, locations, words, count - 1, paths)
        locations.pop()

    return paths


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    board = BoardObject(board)
    word = ""
    path_length = len(path)
    unique_path = set(path)
    if len(path) != len(unique_path): # checks to see if the origin path had duplicates locations
        return None
    for loc_index in range(path_length):
        if not board.is_location_in_board(path[loc_index]):
            return None
        elif loc_index< path_length - 1:
            if not board.are_neighbors(path[loc_index], path[loc_index + 1]):
                return None
        loc_row , loc_col = path[loc_index]
        word += board.get_location((loc_row, loc_col))
        if word in words:
            return word
    return None

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    board = BoardObject(board)

    paths: List[Path] = []
    for row in range(board.rows):
        for col in range(board.cols):
            get_n_sized_paths_from_location(board, [(row, col)], words, n, paths)

    return paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass


if __name__ == '__main__':
    board = [["I", "E", "E", "Y"],
             ["E", "B", "I", "W"],
             ["A", "V", "E", "R"],
             ["U", "W", "A", "P"]]

    words = ['EAVE', 'BEAU', 'BEAR', 'WEIR', 'WIVE', 'WIVE',
             'WIRE', 'WEAR', 'WEIR', 'WRAP', 'AVER', 'VIEW',
             'VIEW', 'VIEW', 'EAVE', 'REAP', 'RAVE', 'RAVE',
             'RAPE', 'WAVE', 'WAVE', 'WAVE', 'WAVE', 'WARE',
             'WARP', 'WEAR', 'WEIR', 'AVER', 'PEAR', 'PAVE',
             'PAVE', 'PARE']

    paths = []
    from pprint import pprint as pp

    pp(find_length_n_paths(4, board, words))
    # print(get_n_sized_paths_from_location(board, [(1, 1)], words, 3))
