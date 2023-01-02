#################################################################
# FILE : test_ex9.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex9 2022-2023
#################################################################

from car import Car

VERTICAL = 0
HORIZONTAL = 1
MOVE_UP = "u"
MOVE_DOWN = "d"
MOVE_LEFT = "l"
MOVE_RIGHT = "r"

# TEST CAR
def test_get_name():
    car = Car("a", 2, (0, 0), VERTICAL)
    assert "a" == car.get_name()
    car2 = Car("abra123", 2, (0, 0), VERTICAL)
    assert "abra123" == car2.get_name()


def test_initial_car_coordinates():
    car1 = Car("test", 4, (2,-2), VERTICAL)
    car2 = Car("test", 4, (2,2), HORIZONTAL)
    car3 = Car("test", 1, (2, 2), VERTICAL)
    assert sorted([
        (2,-2), (3,-2), (4,-2), (5,-2)
    ]) == sorted(car1.car_coordinates())
    assert sorted([
        (2,2), (2,3), (2,4), (2,5)
    ]) == sorted(car2.car_coordinates())
    assert sorted([
        (2, 2)
    ]) == sorted(car3.car_coordinates())


def test_possible_moves():
    car = Car("test", 2, (1,4), VERTICAL)
    car2 = Car("test", 4, (1,4), HORIZONTAL)

    possible_moves = set(car.possible_moves().keys())
    assert sorted([MOVE_UP, MOVE_DOWN]) == sorted(possible_moves)
    possible_moves2 = set(car2.possible_moves().keys())
    assert sorted([MOVE_LEFT, MOVE_RIGHT]) == sorted(possible_moves2)


def test_move():
    # moving in valid direction
    car = Car("test", 2, (1,4), VERTICAL)
    coords0 = car.car_coordinates()
    assert car.move(MOVE_UP)
    coords1 = car.car_coordinates()
    assert  sorted(coords1) == [(row-1, col) for row, col in sorted(coords0)]
    assert car.move(MOVE_DOWN)
    coords2 = car.car_coordinates()
    assert coords2 == coords0

    car = Car("test", 3, (1,2), HORIZONTAL)
    coords0 = car.car_coordinates()
    assert car.move(MOVE_RIGHT)
    coords1 = car.car_coordinates()
    assert [(row, col+1) for row,col in sorted(coords0)] == sorted(coords1)
    assert car.move(MOVE_LEFT)
    coords2 = car.car_coordinates()
    assert sorted(coords0) == sorted(coords2)

    # moving in wrong direction
    car = Car("kk", 2, (1,4), VERTICAL)
    coords0 = car.car_coordinates()
    assert not car.move(MOVE_RIGHT)
    assert sorted(coords0) == sorted(car.car_coordinates())
    assert not car.move(MOVE_LEFT)
    assert sorted(coords0) == sorted(car.car_coordinates())

    # moving in non existent direction
    car = Car("kk", 2, (1,4), VERTICAL)
    coords0 = car.car_coordinates()
    assert not car.move("abcd")
    assert sorted(coords0) == sorted(car.car_coordinates())

    # cars have no bound limits
    car = Car("woot", 2, (0, 0), HORIZONTAL)
    assert car.move(MOVE_LEFT)
    assert sorted([(0, -1), (0, 0)]) == sorted(car.car_coordinates())


def test_move_requirements():
    car = Car("oki", 2, (2,4), HORIZONTAL)
    assert sorted([(2,6)]) == sorted(car.movement_requirements(MOVE_RIGHT))
    assert sorted([(2,3)]) == sorted(car.movement_requirements(MOVE_LEFT))

    car = Car("oki", 2, (2,4), VERTICAL)
    assert sorted([(1,4)]) == sorted(car.movement_requirements(MOVE_UP))
    assert sorted([(4,4)]) == sorted(car.movement_requirements(MOVE_DOWN))

# TEST BOARD
from board import Board
from car import Car

VERTICAL = 0
HORIZONTAL = 1
MOVE_UP = "u"
MOVE_DOWN = "d"
MOVE_LEFT = "l"
MOVE_RIGHT = "r"


def test_initial_works():
    board = Board()
    # ensure target_location is as expected
    assert (3, 7) == board.target_location()

    # ensure cell_list begins empty
    assert 7*7+1 == len(board.cell_list())
    for row, col in board.cell_list():
        assert board.cell_content((row, col)) is None

    # no moves without cars
    assert board.possible_moves() == []


def test_add_car():
    board = Board()
    car1 = Car("R", 5, (0, 0), HORIZONTAL)
    assert board.add_car(car1)

    # can't add same car instance twice
    assert not board.add_car(car1)
    # can't add car with same name
    assert not board.add_car(Car("R", 2, (5,5), VERTICAL))

    # can't add car out of bounds
    assert not board.add_car(Car("Y", 1, (0, -1), VERTICAL))
    assert not board.add_car(Car("Y", 1, (-1, 0), HORIZONTAL))
    # can't add car with length that makes it go out of bounds
    assert not board.add_car(Car("Y", 8, (2, 0), HORIZONTAL))
    assert not board.add_car(Car("Y", 7, (1, 4), VERTICAL))
    # can't add car that might collide with car1
    assert not board.add_car(Car("Y", 1, (0, 4), HORIZONTAL))

    # the board isn't aware of limits regarding car names, so this is valid
    car2 = Car("ZO", 2, (5, 5), VERTICAL)
    assert board.add_car(car2)

    # can't add a car that collides with car2
    assert not board.add_car(Car("B", 1, (6, 5), HORIZONTAL))
    assert not board.add_car(Car("B", 2, (4, 5), VERTICAL))

    # ensure none of the cars that should've failed to be added, were added somehow
    # so we should only have have 7 occupied cells(5 from 'R', 2 from 'ZO').
    assert 7 == sum(1 for coord in board.cell_list() if board.cell_content(coord) if coord is not None)


def test_board_str_different_representations():
    # here, we ensure that each operation that changes the board's state to a
    # new one generates a DIFFERENT string (even though we don't know how said string looks like)
    board = Board()
    board_strs = {str(board)}

    assert board.add_car(Car("R", 2, (0, 0), HORIZONTAL))
    board_strs.add(str(board))
    assert board.move_car("R", MOVE_RIGHT)
    board_strs.add(str(board))

    # we performed 3 operations that changed the board(to 3 different states)
    # so we should've seen 3 different strings
    assert 3 == len(board_strs)


def test_cell_content_works():
    board = Board()
    car1 = Car("R", 2, (0,0), HORIZONTAL)
    car2 = Car("Y", 2, (1,1), VERTICAL)
    assert board.add_car(car1)
    assert board.add_car(car2)

    assert "R" == board.cell_content((0, 0))
    assert "R" == board.cell_content((0, 1))
    assert "Y" == board.cell_content((1, 1))
    assert "Y" == board.cell_content((2, 1))

    # the destination (3,7) is considered part of the board:
    winning_car = Car("O", 3, (3,4), HORIZONTAL)
    assert board.add_car(winning_car)
    assert board.move_car("O", MOVE_RIGHT)
    assert "O" == board.cell_content(board.target_location())

    # a horizontal car at (3,6) doesn't necessarily mean it's at (3,7) too
    another_board = Board()
    not_a_winning_car = Car("R", 1, (3, 6), HORIZONTAL)
    assert another_board.add_car(not_a_winning_car)
    assert another_board.cell_content(board.target_location()) is None


def test_possible_moves_works():
    board = Board()

    def car_moves(car_name):
        return sorted(move for name, move, _desc in board.possible_moves() if car_name == name)

    car1 = Car("R", 2, (1, 2), HORIZONTAL)
    car2 = Car("Y", 2, (3, 3), VERTICAL)
    assert board.add_car(car1)
    assert board.add_car(car2)
    assert car_moves("R") == sorted([MOVE_LEFT, MOVE_RIGHT])
    assert car_moves("Y") == sorted([MOVE_UP, MOVE_DOWN])

    blocking_r_from_left = Car("O", 2, (1, 0), HORIZONTAL)
    assert board.add_car(blocking_r_from_left)
    assert car_moves("R") == sorted([MOVE_RIGHT])
    assert [] == car_moves("O")

    blocking_y_from_down = Car("Wut", 1, (5, 3), HORIZONTAL)
    assert board.add_car(blocking_y_from_down)
    assert car_moves("Y") == sorted([MOVE_UP])
    assert car_moves("Wut") == sorted([MOVE_LEFT, MOVE_RIGHT])


def test_move_car():
    board = Board()

    def get_car_cords(car_name):
        return sorted(coord for coord in board.cell_list() if board.cell_content(coord) == car_name)

    car1 = Car("R", 2, (0, 0), HORIZONTAL)
    car2 = Car("Y", 2, (1, 0), VERTICAL)
    assert board.add_car(car1)
    assert board.add_car(car2)

    assert sorted([(0,0), (0, 1)]) == get_car_cords("R")
    assert sorted([(1, 0), (2, 0)]) == get_car_cords("Y")

    # can't move left as car1 is blocked by the board's bounds
    assert not board.move_car("R", MOVE_LEFT)
    assert sorted([(0, 0), (0, 1)]) == get_car_cords("R")

    # can't move car2 up as it's blocked by car1
    assert not board.move_car("Y", MOVE_UP)
    assert sorted([(1, 0), (2, 0)]) == get_car_cords("Y")

# TEST GAME
import sys
import tempfile
import json
import os
from pathlib import Path
from subprocess import Popen, PIPE


class Helper:
    def __init__(self, log=False):
        self._game_py = str(Helper.__find_game_py())
        self._python = sys.executable
        if log:
            print()
            print(f"Using game.py at {self._game_py}")
            print(f"Using python executable at {self._python}")
            print()

    def _run_game_process(self, json_file, input_txt):
        args = [self._python, self._game_py, json_file]
        _, err = Popen(args, universal_newlines=True, stdin=PIPE,
                       stderr=PIPE).communicate(input_txt)

        # check for other errors(e.g compilation errors, type errors) that aren't
        # related to whether the program has finished successfully or not.
        if len(err) > 0 and "EOF" not in err:
            raise Exception(f"There was an unexpected error while running this test:\n"
                            f"Error message from your executing your program:\n\n{err}\n"
                            f"(this is a problem with your code)")
        return err

    def finishes_with_exact_moves(self, car_cfg, moves):

        # first I check that the given moves result in the program finishing
        # successfully
        moves_st = "\n".join(moves)
        err = self._run_game_process(car_cfg, moves_st)
        assert len(err) == 0, "The game should've terminated successfully after being given " \
                              "all valid moves, but instead it expected for more input."

        # Since the process library doesn't know if all standard input has been consumed/processed, I make another
        # test to ensure that we don't win when given less than the needed moves to win.
        if len(moves) == 0:
            return
        not_enough_moves_st = "\n".join(moves[:-1])
        err = self._run_game_process(car_cfg, not_enough_moves_st)
        assert "EOF" in err, "When providing less than the exact moves for victory, the game should've " \
                             "errored(as it should expect for more input), but it has terminated successfully " \
                             "as if we have won."

    def fails_with_given_moves(self, car_cfg, moves):
        moves_st = "\n".join(moves)
        err = self._run_game_process(car_cfg, moves_st)
        # we expect an EOF error as we interrupted the process while it should've
        # waited for more input()
        assert "EOF" in err, "The game has terminated successfully despite not giving "\
                             "it enough moves to win! It should've expected more input"

    @staticmethod
    def __find_game_py():
        return "game.py"


def test_ensure_tests_configured_corrrectly():
    _test_helper = Helper(log=True)


def create_car_config(cars_dict):
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(bytes(json.dumps(cars_dict), 'UTF-8'))
        return file.name


def test_valid_simple():
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    if os.getcwd() != source_dir:
        os.chdir(source_dir)
    cars = {
        "R": [2, [3, 0], 1],
        "O": [3, [1, 4], 0]
    }

    cfg_file = create_car_config(cars)
    test_helper = Helper()

    test_helper.finishes_with_exact_moves(cfg_file, ["O,u"] + ["R,r"] * 6)
    test_helper.finishes_with_exact_moves(
        cfg_file, ["O,u"] + ["R,r"] * 5 + ["R,l", "R,r", "R,r"])
    test_helper.finishes_with_exact_moves(
        cfg_file, ["O,u"] + ["Invalid,Cowabunga"] * 10 + ["O,u"] * 10 + ["R,r"] * 6)
    test_helper.finishes_with_exact_moves(
        cfg_file, ["O,u"] + ["Invalid command"] * 10 + ["R,r"] * 6)
    test_helper.finishes_with_exact_moves(
        cfg_file, ["O,u"] + ["Invalid command"] * 10 + ["R,r"] * 3 + ["!"])

    test_helper.fails_with_given_moves(cfg_file, ["O,u"] + ["R,r"] * 2)
    test_helper.fails_with_given_moves(cfg_file, ["O,u"] + ["R,r"] * 1)

    # automatic win
    cars = {
        "R":[2,[3,6],1]
    }
    cfg_file = create_car_config(cars)
    test_helper.finishes_with_exact_moves(cfg_file, [])

    cars = {
        "R": [2, [3, 3], 1],
        "W": [2, [0, 0], 1],
        "Y": [3, [1, 6], 0],
        "O": [-3, [1, 6], 0],
        "B": [3, [1, -6], 0],
        "G": [3, [1, -6], 2],
        "GG": [2, [3, 0], 0]
    }

    cfg_file = create_car_config(cars)

    test_helper.finishes_with_exact_moves(cfg_file, ["Y,u"] + ["R,r"] * 3)
    test_helper.finishes_with_exact_moves(
        cfg_file, ["Y,d"] * 3 + ["R,r"] * 2 + ["R,l", "R,r", "R,r"])
    test_helper.finishes_with_exact_moves(
        cfg_file, ["Y,u"] + ["Invalid,Cowabunga"] * 10 + ["O,u"] * 10 + ["R,r"] * 3)
    test_helper.finishes_with_exact_moves(
        cfg_file, ["Y,d"] * 3 + ["Invalid command"] * 10 + ["R,r"] * 3)

    test_helper.fails_with_given_moves(cfg_file, ["O,u"] + ["R,r"] * 3)
    test_helper.fails_with_given_moves(cfg_file, ["Y,u"] + ["R,r"] * 2)
