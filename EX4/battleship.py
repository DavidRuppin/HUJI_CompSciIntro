from typing import List, Tuple, Optional

import helper

from helper import NUM_ROWS, NUM_COLUMNS, SHIP_SIZES, WATER, SHIP, HIT_WATER, HIT_SHIP


# HELPER  FUNCTIONS #
def is_str_pos_int(num_str: str) -> bool:
    # Returns True if @num_str is a string representation of a positive integer else False
    return True if helper.is_int(num_str) and int(num_str) > 0 else False


def is_pos_int(sus_int: str) -> bool:
    # Returns True if @sus_int is a positive integer else False
    return True if type(sus_int) is int and int(sus_int) > 0 else False


def place_object(board, mark: int, loc: tuple, size: int = 1) -> List:
    # Helper function that places any objet vertically in the board. !!ASSUMING LEGITIMATE PARAMETERS!!
    for row in range(loc[0], loc[0] + size):
        board[row][loc[1]] = mark

    return board


def is_loc_in_board(board, loc: tuple) -> bool:
    # returns True if @loc is within the board else False
    return True if len(board) >= loc[0] >= 0 and len(board[0]) >= loc[1] >= 0 else False


def get_loc_in_board(board, loc) -> int:
    return board[loc[0]][loc[1]] if is_loc_in_board(board, loc) else None


def censor_board(board):
    new_board = []
    for row in board:
        new_board.append([item if item != SHIP else WATER for item in row])

    return new_board


# END OF HELPER FUNCTIONS #

def init_board(rows, columns) -> Optional[List[List[int]]]:
    # Returns a board of rows x columns of Water
    if is_pos_int(rows) and is_pos_int(columns):
        return [[WATER for col in range(columns)] for row in range(rows)]
    return None


def cell_loc(name: str) -> Optional[Tuple[int, int]]:
    # Making sure the input is 2-3 characters and is a string
    if 3 >= len(name) >= 2 and type(name) is str:
        # Making sure there's a character and an int ONLY in the input
        if name[0].isalpha() and is_str_pos_int(name[1:]):
            col = ord(name[0].upper()) - ord("A")
            row = int(name[1:]) - 1
            return row, col

    return None


def valid_ship(board, size, loc) -> bool:
    # Checking that the final cell of the ship is in the board
    if not is_loc_in_board(board, (loc[0] + size, loc[1])):
        return False
    #  Checking that the initial location is legal
    if not is_loc_in_board(board, loc):
        return False

    # Checking that every destined cell is available
    for row in range(size):
        if board[loc[0] + row][loc[1]] != WATER:
            return False

    return True


def fire_torpedo(board, loc):
    # Checking if the location is legitimate, then placing a torpedo accordingly
    if is_loc_in_board(board, loc):
        cell = get_loc_in_board(board, loc)
        # Placing HIT_WATER or HIT_SHIP appropriately
        if cell == WATER:
            board = place_object(board, HIT_WATER, loc)
        elif cell == SHIP:
            board = place_object(board, HIT_SHIP, loc)
    return board


def create_player_board(rows, columns, ship_sizes):
    board = init_board(rows, columns)
    for ship_size in ship_sizes:
        loc = None
        while loc is None or not valid_ship(board, ship_size, loc):
            helper.print_board(board)
            cell_input = helper.get_input(
                "enter top coordinate for a ship of size {} in range (A1-Z99): ".format(ship_size))
            loc = cell_loc(cell_input)
            if loc is None:
                print("Not a valid input")
            elif not valid_ship(board, ship_size, loc):
                print("Not a valid location")

        board = place_object(board, SHIP, loc, ship_size)

    return board


def create_computer_board(rows, cols, ship_sizes):
    board = init_board(rows, cols)
    for ship_size in ship_sizes:
        # Creating a list of all the available locations using the @valid_ship function to check availability of each
        locations = set((row, col) for row in range(rows) for col in range(cols) if
                        valid_ship(board, ship_size, (row, col)))
        # Choosing a random location and placing the ship there
        loc = helper.choose_ship_location(board, ship_size, locations)
        board = place_object(board, SHIP, loc, ship_size)

    return board


def random_torpedo_location(board) -> Optional[Tuple[int, int]]:
    # Finds all the locations that haven't been hit yet
    locations = set((row, col) for row in range(len(board)) for col in range(len(board[0])) if
                    get_loc_in_board(board, (row, col)) not in [HIT_SHIP, HIT_WATER])

    # If there are locations to bomb choose one randomly, else return None
    if locations:
        return helper.choose_torpedo_target(censor_board(board), locations)
    return None


def is_game_over(board) -> bool:
    # Checking if there's a single ship left. If there is game's not over
    for row in board:
        for obj in row:
            if obj == SHIP:
                return False

    # Game's over baby
    return True


def computer_play_turn(player_board):
    # Fires a single, random torpedo
    fire_torpedo(player_board, random_torpedo_location(player_board))


def player_play_turn(player_board, computer_board):
    # Let's player fire a single torpedo after seeing the boards
    helper.print_board(player_board, censor_board(computer_board))
    loc = None
    while loc is None:
        decision = helper.get_input("Where would you like to bomb commander? (A1-Z99): ")
        loc = cell_loc(decision)
        if loc is None:
            print("Invalid input ")

    fire_torpedo(computer_board, loc)


def play_turn(player_board, computer_board):
    # Play player then computer
    player_play_turn(player_board, computer_board)
    computer_play_turn(player_board)


def get_display_game_results(player_board, computer_board):
    helper.print_board(player_board, censor_board(computer_board))
    player_down, computer_down = is_game_over(player_board), is_game_over(computer_board)
    if player_down and computer_down:
        return "Mutual destruction! Better luck next time.\nTIE"
        pass
    elif player_down:
        return "Oof, that's gotta hurt...\nCOMPUTER WINS"
        pass
    elif computer_down:
        return "BEEP-BOOP~ SYSTEMS SHUTTING DOWN~ SINKING INTO THE ABYSS~ TELL MY WIFE I LOVED HER~\nPLAYER WINS"
        pass


def main():
    player_board = create_player_board(NUM_ROWS, NUM_COLUMNS, SHIP_SIZES)
    computer_board = create_computer_board(NUM_ROWS, NUM_COLUMNS, SHIP_SIZES)

    while not is_game_over(player_board) and not is_game_over(computer_board):
        play_turn(player_board, computer_board)

    again = None
    while again is None:
        decision = helper.get_input(f"{get_display_game_results(player_board, computer_board)}\nPlay again? (Y/N): ")
        if decision.upper() == "Y":
            main()
        elif decision.upper() == "N":
            return
        print("Invalid input ")


if __name__ == "__main__":
    NUM_ROWS = 2
    NUM_COLUMNS = 3
    SHIP_SIZES = [2, 2]
    main()
