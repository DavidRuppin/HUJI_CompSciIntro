import argparse
from typing import Optional
from game_display import GameDisplay

from game_objects import *


class SnakeGame:

    def __init__(self, args: argparse.Namespace) -> None:
        self.board_limit = Location(args.height, args.width)
        self.num_of_apples = args.apples
        self.rounds = args.rounds
        self.__key_clicked = None
        self.snake = Snake(Location(args.height // 2, args.width // 2))
        self.apples = {}
        # FIXME - This is purely for tests
        self.snake.extend_rear(Location(4, 5))
        self.apples = {Location(i, i) for i in range(20)}
        self.eaten = 0

    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked


    def move_snake(self):
        do_pop = True
        if self.eaten > 0:
            do_pop = False
            self.eaten -= 1
        self.snake.move(do_pop)
    def update_objects(self) -> None:
        if self.__key_clicked == 'Left':
            self.snake.rotate_left()
        elif self.__key_clicked == 'Right':
            self.snake.rotate_right()

        self.move_snake()

        if self.has_snake_head_crashed():
            raise ValueError(f'Snake head reached {self.snake.get_head_location()}, a crash!'
                             f'\n The board\'s limit is {self.board_limit}')


        if self.snake.get_head_location() in self.apples:
            self.apples.remove(self.snake.get_head_location())
            self.eaten += 3

    def has_snake_head_crashed(self) -> bool:
        """Checks if the snake head crashed into itself or went out of bounds. Does NOT test walls"""
        head = self.snake.get_head_location()
        if head in self.snake.get_locations():
            return True
        elif head < Location(0, 0) or head >= self.board_limit:
            return True

        return False

    def draw_board(self, gd: GameDisplay) -> None:
        for loc in self.snake.get_entire_snake():
            gd.draw_cell(loc.col, loc.row, "blue")
        for loc in self.apples:
            gd.draw_cell(loc.col, loc.row, "green")

    def get_unavailable_locations(self):
        return self.snake.get_entire_snake()

    def get_score(self):
        return len(self.snake.get_entire_snake())

    def end_round(self) -> None:
        pass

    def is_over(self) -> bool:
        return False
