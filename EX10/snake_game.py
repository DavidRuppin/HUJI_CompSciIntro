import argparse
from typing import Optional, Set

from EX10 import game_utils
from game_display import GameDisplay

from game_objects import *


class SnakeGame:

    def __init__(self, args: argparse.Namespace) -> None:
        self.board_limit = Location(args.height, args.width)
        self.apples = args.apples
        self.rounds = args.rounds
        self.__key_clicked = None
        self.init_snake(args.width, args.height, args.debug)
        self.apple_set = set()
        self.debug = args.debug

        self.eaten = 0
        self.score_tracker = ScoreTracker()

    def init_snake(self, width: int, height: int, debug: bool):
        starting_location = Location(height // 2, width // 2)
        if debug:
            starting_location = Location(-1, -1)
        self.snake = Snake(starting_location)


    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked

    def move_snake(self):
        do_pop = True
        # If the snake hasn't 'consumed all the calories' from the apple, keep extending it
        if self.eaten > 0:
            do_pop = False
            self.eaten -= 1
        self.snake.move(do_pop)

    def handle_snake_movement(self):
        if self.__key_clicked == 'Left':
            self.snake.rotate_left()
        elif self.__key_clicked == 'Right':
            self.snake.rotate_right()


        self.move_snake()

        if self.has_snake_head_crashed():
            raise ValueError(f'Snake head reached {self.snake.get_head_location()}, a crash!'
                             f'\n The board\'s limit is {self.board_limit}')

    def increase_score_from_apple(self):
        self.score_tracker.increase_score(ScoreTracker.get_score_increment(len(self.snake.get_entire_snake())))

    def generate_apple(self) -> bool:
        """
        Attempts to generate an apple and place it randomly, if the location is unavailable, don't
        @return: True on success, False on failure
        """
        col, row = game_utils.get_random_apple_data()
        apple_loc = Location(row, col)
        if self.is_location_in_board(apple_loc) and apple_loc not in self.get_used_locations():
            self.apple_set.add(apple_loc)
            return True

        return False

    def update_objects(self) -> None:
        print(self.apple_set)
        if self.apples > len(self.apple_set):
            self.generate_apple()

        if self.debug is False:
            self.handle_snake_movement()

            # If the snake eats an apple increase the eaten counter
            if self.snake.get_head_location() in self.apple_set:
                self.apple_set.remove(self.snake.get_head_location())
                self.increase_score_from_apple()
                self.eaten += 3

    def has_snake_head_crashed(self) -> bool:
        """Checks if the snake head crashed into itself or went out of bounds. Does NOT test walls"""
        head = self.snake.get_head_location()
        if head in self.snake.get_locations() or not self.is_location_in_board(head):
            return True

        return False

    def is_location_in_board(self, location: Location) -> bool:
        """Checks whether a given location is within the boundaries of the boar"""
        return location >= Location(0, 0) and location <= self.board_limit

    def draw_board(self, gd: GameDisplay) -> None:
        for loc in self.snake.get_entire_snake():
            gd.draw_cell(loc.col, loc.row, "blue")
        for loc in self.apple_set:
            gd.draw_cell(loc.col, loc.row, "green")

    def get_used_locations(self) -> Set[Location]:
        """Returns a set of locations that are occupied by objects (Snake, Apples, Walls}"""
        return {*self.snake.get_entire_snake(), }.union(self.apple_set)

    def get_score(self):
        return self.score_tracker.get_score()

    def end_round(self) -> None:
        pass

    def is_over(self) -> bool:
        return False
