from functools import lru_cache
from typing import List, Tuple, Iterable, Optional, Set

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = Tuple[int, int]

class BoardObject:
    def __init__(self, board: Board):
        self._board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self) -> Board:
        return self._board

    def get_num_rows(self) -> int:
        return self.rows

    def get_num_cols(self) -> int:
        return self.cols

    @lru_cache()
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
        word = self.word_from_locations(path)
        return word if word in words else None

    def get_location(self, location: Location) -> str:
        row, col = location
        return self._board[row][col]

    def word_from_locations(self, locations: Path) -> Optional[str]:
        return ''.join(self.get_location(location) for location in locations)



def load_boggle_dictionary(file_name : str) -> Iterable[str]:
    with open(file_name,'r') as f:
        words = [line.strip() for line in f.readlines()]
        set_words = set(words)
        return set_words

@lru_cache()
def create_partial_words_from_word(word: str) -> Set[str]:
    return {word[:i] for i in range(1, len(word) + 1)}


def create_partial_words(words: Iterable[str]) -> Set[str]:
    """
    returns : a set of all prefixes of words that exists in the boggle_dict.txt file
    the purpose is to optimize the find_n_length_paths function so that we can cancel brances
    before the end. during find_n_length_paths we create partial words, but of the partial word is not in
    the set of prefixes, we can stop and not check all the variations of this word\path.
    """
    res = set()
    for word in words:
        res.update(create_partial_words_from_word(word))
    return res

def get_n_sized_paths_from_location(board: BoardObject, locations: Path, partial_word_set: Set[str],
                                    words: Iterable[str], count,
                                    paths: List[Path]) -> List[Path]:
    if type(words) is not set:
        words = set(words)

    # Get all the paths from the last location in the @locations list [which is the tail of the current path]
    if count == 1:
        if board.is_path_valid(locations, words):
            paths.append([*locations])
        return

    for neighbor in board.get_location_neighbors(locations[-1]):
        if neighbor in locations:
            continue

        locations.append(neighbor)
        # If we're near the end check first then send to the final check
        if board.word_from_locations(locations) in partial_word_set or count == 2:
            get_n_sized_paths_from_location(board, locations, partial_word_set, words, count - 1, paths)
        locations.pop()

    return paths


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    board = BoardObject(board)
    word = ""
    path_length = len(path)
    unique_path = set(path)
    if len(path) != len(unique_path):  # checks to see if the origin path had duplicates locations
        return None

    for loc_index in range(path_length):
        if not board.is_location_in_board(path[loc_index]):
            return None
        elif loc_index < path_length - 1:
            if not board.are_neighbors(path[loc_index], path[loc_index + 1]):
                return None
        loc_row, loc_col = path[loc_index]
        word += board.get_location((loc_row, loc_col))

    return word if word in words else None


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    return find_length_n_paths_with_options(n, board, set(words))


def find_length_n_paths_with_options(n: int, board: Board, words: Iterable[str], partial_word_set=None) -> List[Path]:
    board = BoardObject(board)
    if partial_word_set is None:
        partial_word_set = create_partial_words(words)

    paths: List[Path] = []
    for row in range(board.rows):
        for col in range(board.cols):
            get_n_sized_paths_from_location(board, [(row, col)], partial_word_set, words, n, paths)

    return paths


def _find_length_n_words_helper(n: int, board: BoardObject, words: Iterable[str], count: int, path: Path,
                                partial_words: Set[str],
                                paths: List[Path]):
    if len(board.word_from_locations(path)) == n and is_valid_path(board.get_board(), path, words):
        paths.append([*path])
        return paths
    elif count == 0:
        return

    for location in board.get_location_neighbors(path[-1]):
        path.append(location)
        if board.word_from_locations(path) in partial_words:
            _find_length_n_words_helper(n, board, words, count - 1, path, partial_words, paths)
        path.pop()
    return paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    partial_words = create_partial_words(words)
    board: BoardObject = BoardObject(board)
    paths: List[Path] = []
    for row in range(board.rows):
        for col in range(board.cols):
            _find_length_n_words_helper(n, board, words, n, [(row, col)], partial_words, paths)
    return paths


def add_results(board: BoardObject, all_paths: List[Path], cur_results: List[Path], words_chosen: List[str]):
    """
    this function checks if the new paths that were found were paths for words that have been calcuated
    and added already to the final list of paths. It doesnt have to check if the score for the current path
    is bigger from the path that exists already because the outer loop in max score iterated from the longest
    path options to the shortest so if the word that represents the path already exists it means
    that for this words there is already a longer path and therefore the current path shoud not be added.
    """
    for path in cur_results:
        word = board.word_from_locations(path)
        if word in words_chosen:
            continue
        all_paths.append(path)
        words_chosen.append(word)



def calcuate_longest_word(words: Iterable[str]):
    """
    checks which is the longest word so the function max score won't need to iterate through
    the longest possible path in the board
    """
    return max(map(lambda word : len(word), words))



def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:

    board: BoardObject = BoardObject(board)
    words_chosen = []
    all_paths = []

    partial_word_set = create_partial_words(words)
    # every iteration return and add all possible paths with length of "n"
    for n in range(calcuate_longest_word(words), 0, - 1):
        cur_results = find_length_n_paths_with_options(n, board.get_board(), words, partial_word_set)
        # add only the paths that returns max result
        add_results(board, all_paths, cur_results, words_chosen)
    return all_paths
