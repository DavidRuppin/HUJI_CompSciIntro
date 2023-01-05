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
        self.snake = Snake(Location(args.height // 2 , args.width // 2))
        self.snake.extend_rear(Location(4, 5))
        self.apples = {Location(i, i) for i in range(20)}

    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked

    def update_objects(self) -> None:
        if self.__key_clicked == 'Left':
            self.snake.rotate_left()
        elif self.__key_clicked == 'Right':
            self.snake.rotate_right()
        popped = self.snake.move()

        if self.has_snake_head_crashed():
            raise ValueError(f'Snake head reached {self.snake.get_head_location()}, a crash!'
                             f'\n The board\'s limit is {self.board_limit}')

        if popped in self.apples:
            self.apples.remove(popped)
            self.snake.extend_rear(popped)

    def has_snake_head_crashed(self) -> bool:
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
            gd.draw_cell(loc.col, loc.row, "red")

    def end_round(self) -> None:
        pass

    def is_over(self) -> bool:
        return False
