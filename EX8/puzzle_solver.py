from typing import List, Tuple, Set, Optional

# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    if picture[row][col] == 0:
        return 0

    # Iterating over the column
    col_sum = 0
    for x in range(len(picture)):
        if picture[x][col] == 0:
            if x < row:
                col_sum = 0
            if x > row:
                break
        else:
            col_sum += 1

    # Iterating over the row
    row_sum = 0
    for y in range(len(picture[0])):
        if picture[row][y] == 0:
            if y < col:
                row_sum = 0
            if y > col:
                break
        else:
            row_sum += 1

    # Not to count (row, col) twice
    row_sum -= 1

    return row_sum + col_sum


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    # Creating a new board where the 0's and -1's are both 0's and the 1's stay 1's
    new_board = [[1 if item == 1 else 0 for item in row_iterator] for row_iterator in picture]
    return max_seen_cells(new_board, row, col)


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    res = 1

    for constraint in constraints_set:
        row, col, seen = constraint
        min_seen, max_seen = min_seen_cells(picture, row, col), max_seen_cells(picture, row, col)

        if min_seen <= seen <= max_seen and min_seen != max_seen:
            res = 2
        elif seen < min_seen or seen > max_seen:
            return 0

    return res


def get_relevant_constraints(constraint_set: Set[Constraint], row: int, col: int) -> Set[Constraint]:
    return constraint_set


def init_board(rows: int, cols: int) -> Picture:
    """
    Creates a new 'unknown' board (unknown being -1)

    @param rows: The height of the new board
    @param cols: The width of the new board
    @return: Picture initialized with -1's all around
    """
    return [[-1 for col in range(cols)] for row in range(rows)]


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    """

    @param constraints_set: The set of constraints we must enforce
    @param n: The number of rows in the new board
    @param m: The number of columns in the new board
    @return: A solved Picture if possible, None if no board can be created
    """
    return solve_puzzle_helper(init_board(n, m), constraints_set)


def solve_puzzle_helper(board: Picture, constraint_set: Set[Constraint], index: int = 0) -> Optional[Picture]:

    # Getting the current row and column from the index
    row, col = index // len(board[0]), index % len(board[0])

    # Getting only the relevant constraints for the current row and col
    constraints = get_relevant_constraints(constraint_set, row, col)
    constraint_result = check_constraints(board, constraints)

    # If the board is solved, needs debugging
    if constraint_result == 1:
        return board
    # Or if there's an error
    elif constraint_result == 0:
        return None
    # If the board is complete

    for value in [0, 1]:
        board[row][col] = value
        res = solve_puzzle_helper(board, constraint_set, index + 1)

        if type(res) is list:
            return res

    board[row][col] = -1


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    ...


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    ...
