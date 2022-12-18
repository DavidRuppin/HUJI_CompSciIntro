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


def check_board_complete(board: Picture) -> bool:
    return not bool(sum([row.count(-1) for row in board]))


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
    if constraint_result == 1 and check_board_complete(board):
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
    return None


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    """
    Like solve_puzzle except instead of returning a singular solution this function counts and returns the amount of
    possible solutions to a given puzzle (0 being no solutions found
    @param constraints_set: The constraints we must adhere to
    @param n: The number of rows
    @param m: The number of columns
    @return: Solution count
    """

    return solution_count_helper(init_board(n, m), constraints_set)


def solution_count_helper(board: Picture, constraint_set: Set[Constraint], index: int = 0) -> int:
    # Getting the current row and column from the index
    row, col = index // len(board[0]), index % len(board[0])

    # Getting only the relevant constraints for the current row and col
    constraints = get_relevant_constraints(constraint_set, row, col)
    constraint_result = check_constraints(board, constraints)

    # If the board is solved, needs debugging
    if constraint_result == 1 and check_board_complete(board):
        return 1
    # Or if there's an error
    elif constraint_result == 0:
        return 0
    # If the board is complete

    res = 0
    for value in [0, 1]:
        board[row][col] = value
        res += solution_count_helper(board, constraint_set, index + 1)

    board[row][col] = -1

    return res


def get_seen_count(board: Picture, row: int, col: int) -> int:
    return max_seen_cells(board, row, col)


def is_constrained(board: Picture, row: int, col: int, constraints: Set[Constraint]) -> bool:
    """
    If one of the constraints is relevant to board[row][col] return True, else False
    @param row, col: The coordinate to check
    @param constraints: A set of constraints
    @return:
    """

    if board[row][col] == 0:
        return False

    for constraint in constraints:
        if constraint[0] != row and constraint[1] != col:
            continue

        if constraint[0] == row and constraint[2] >= abs(col - constraint[1]):
            return True
        elif constraint[1] == col and constraint[2] >= abs(row - constraint[0]):
            return True

    return False


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    """
    Iterating over the give picture and adds the minial amount of constraints to create a puzzle
    """
    constraints: Set[Constraint] = set()
    for row in range(len(picture)):
        for col in range(len(picture[0])):
            if is_constrained(picture, row, col, constraints):
                continue
            constraints.add((row, col, get_seen_count(picture, row, col)))

    return constraints
