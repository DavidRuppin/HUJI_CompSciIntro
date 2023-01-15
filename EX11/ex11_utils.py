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
    @lru_cache
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


@lru_cache
def create_partial_words_from_word(word: str) -> Set[str]:
    return {word[:i] for i in range(1, len(word)+1)}


def create_partial_words(words: Iterable[str]) -> Set[str]:
    res = set()
    for word in words:
        res.update(create_partial_words_from_word(word))
    return res
# def create_partial_words(words: Iterable[str]) -> Set[str]:
#     max_length = max(map(lambda x: len(x), words))
#     result = set()
#     for iter in range(1, max_length + 1):
#         setter = (set(map(lambda x: x[:iter], words)))
#         result = result.union(setter)
#     return result


def get_n_sized_paths_from_location(board: BoardObject, locations: Path, partial_word_set: Set[str],
                                    words: Iterable[str], count,
                                    paths: List[Path]) -> List[Path]:
    # Get all the paths from the last location in the @locations list [which is the tail of the current path]
    if count == 1:
        if is_valid_path(board._board, locations, words):
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

def find_length_n_paths_with_options(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    return find_length_n_paths_with_options(n, board, words)
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
            _find_length_n_words_helper(n, board, words, count - 1, path, partial_words,paths)
        path.pop()
    return paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    partial_words = create_partial_words(words)
    board :BoardObject = BoardObject(board)
    paths : List[Path] = []
    for row in range(board.rows):
        for col in range(board.cols):
            _find_length_n_words_helper(n, board, words, n, [(row,col)], partial_words, paths)
    return paths


def add_results(board : BoardObject ,all_paths: list[Path], cur_results: List[Path], words_chosen : List[str]):
    for path in cur_results:
        word = board.word_from_locations(path)
        if word in words_chosen:
            continue
        all_paths.append(path)
        words_chosen.append(word)


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    board : BoardObject = BoardObject(board)
    words_chosen = []
    all_paths = []

    partial_word_set = create_partial_words(words)

    for n in range(board.rows * board.cols, 0 , - 1):
        cur_results = find_length_n_paths_with_options(n, board.get_board(), words, partial_word_set)
        add_results(board, all_paths, cur_results, words_chosen)
    return all_paths



if __name__ == '__main__':  # LED", "SITE", "KIT", "WIELD
    BOARD1 = [["I", "S", "W", "L"],
              ["I", "I", "T", "R"],
              ["E", "K", "E", "D"],
              ["A", "M", "L", "J"]]
    BOARD2 = [["I", "E", "E", "Y"],
              ["E", "B", "I", "W"],
              ["A", "V", "E", "R"],
              ["U", "W", "A", "P"]]
    BOARD3 = [["?", "A", "?", "?"],
              ["?", "B", "?", "A"],
              ["?", "C", "B", "?"],
              ["?", "?", "?", "?"]]

    from pprint import pp

    board = BOARD1
    n = 1
    words = []


    def a():
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

        pp(find_length_n_paths_with_options(4, board, words))
        # print(get_n_sized_paths_from_location(board, [(1, 1)], words, 3))


    def b():
        n = 7
        board = [["X", "Z", "Y", "X"],
                 ["Y", "AB", "X", "Z"],
                 ["X", "C", "BA", "?"],
                 ["?", "?", "?", "?"]]
        words = ['ZABCBAZ', 'ZBACABZ', 'XYXCXYX']

        print(find_length_n_paths_with_options(n, board, words))


    def palindrome():
        board = BOARD3
        n = 5
        words = ['ABCBA']
        pp(find_length_n_paths_with_options(n, board, words))


    def happy():
        n, board, words = 4, BOARD1, ["LED", "SITE", "KIT", "WIELD"]
        pp(find_length_n_paths_with_options(n, board, words))


    happy()