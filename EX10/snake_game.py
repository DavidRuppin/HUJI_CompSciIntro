#################################################################
# FILE : snake_game.py
# WRITER 1: David Ruppin, ruppin, 322296336
# WRITER 2: Shachar Cohen, 206532418
# EXERCISE : intro2cs ex10 2022-2023
#################################################################

'''DESCRIPTION: snake_game.py module contains SnakeGame class, which operates the game.'''

#######################   IMPORTS   #############################
import argparse
from typing import Optional, Set

import game_utils
from game_display import GameDisplay

from game_objects import *


#################################################################


class SnakeGame:

    def __init__(self, args: argparse.Namespace) -> None:
        self.board_limit = Location(args.height - 1, args.width - 1)

        # game parameters set by the user
        self.apples = args.apples
        self.walls = args.walls
        self.rounds = args.rounds
        self.debug = args.debug

        # game parameters set by us
        self.__key_clicked = None
        self.init_snake(args.width, args.height, args.debug)
        self.apple_set = set()
        self.wall_list: List[Wall] = []
        self.eaten = 0
        self.score_tracker = ScoreTracker()
        self.round_manager = RoundManager(args.rounds)
        self.event_counter = 0

    ################### SNAKE FUNCTIONS #######################
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
            self.finish_game()

    def has_snake_head_crashed(self) -> bool:
        """Checks if the snake head crashed into itself or went out of bounds. Does NOT test walls"""
        head = self.snake.get_head_location()
        if head in self.snake.get_locations() or not self.is_location_in_board(head):
            return True
        return False

    def handle_collision(self, hit_location_list: Location):
        '''Updates the snake after hitting wall'''
        self.snake.snip_body(hit_location_list)
        if len(self.snake.get_locations()) == 0:
            self.eaten = 0
            self.finish_game()

    ################### SCORE TRACKER FUNCTIONS #######################
    def increase_score_from_apple(self):
        self.score_tracker.increase_score(ScoreTracker.get_score_increment(len(self.snake.get_entire_snake())))

    ################### APPLE FUNCTIONS #######################
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

    def get_used_locations(self) -> Set[Location]:
        """Returns a set of locations that are occupied by objects (Snake, Apples, Walls}"""
        used_locations = {*self.snake.get_entire_snake(), }.union(self.apple_set)

        for wall in self.wall_list:
            used_locations = used_locations.union(set(wall.get_locations()))

        return used_locations

    def remove_apples_wall_intersection(self) -> None:
        '''Removes the apples that intersect with heads of walls'''
        apples_intersection = {wall.get_head_location() for wall in self.wall_list}.intersection(self.apple_set)
        for apple in apples_intersection:
            self.apple_set.remove(apple)

    ################### WALL FUNCTIONS #######################
    def generate_wall(self) -> bool:
        """
        Attempts to generate a wall and place it randomly, if the location is unavailable, don't
        @return: True on success, False on failure
        """
        wall = Wall()
        if {*wall.get_locations()}.intersection(self.get_used_locations()) == set():
            self.wall_list.append(wall)
            return True
        return False

    def move_walls(self) -> None:
        for wall in self.wall_list:
            wall.move()

    def is_wall_aberrant(self, wall) -> bool:
        """Checks if the wall is out of bounds"""
        for loc in wall.get_locations():
            if self.is_location_in_board(loc):
                return False
        return True

    def delete_aberrant_walls(self):
        """"Deletes walls that are totally out of bounds"""
        self.wall_list = [wall for wall in self.wall_list if not self.is_wall_aberrant(wall)]

    def snake_head_hits_wall(self) -> bool:
        """Checks whether the snake's head hit a wall"""
        for wall in self.wall_list:
            if self.snake.get_head_location() in wall.get_locations():
                return True
        return False

    def snake_body_hits_wall_head(self) -> Union[Location, bool]:
        """Returns the 'hit' location in case of a collision, otherwise False"""
        for wall in self.wall_list:
            intersection = {*self.snake.get_entire_snake()}.intersection({*wall.get_locations()})
            if intersection:
                # Return the intersected location
                return intersection.pop()
        return False

    ############# GENERAL FUNCTIONS ############
    def update_objects(self) -> None:
        print(self.snake.get_entire_snake())
        # moves walls on even rounds
        if self.event_counter > 0 and self.event_counter % 2 == 0:
            self.move_walls()
        self.delete_aberrant_walls()  # deletes walls that goes beyond the board
        self.event_counter += 1

        #  generates a new wall every round
        if self.walls > len(self.wall_list):
            self.generate_wall()

        # adds apples
        if self.apples > len(self.apple_set):
            self.generate_apple()

        self.remove_apples_wall_intersection()

        # moves snake
        if self.debug is False:
            self.handle_snake_movement()

            head = self.snake.get_head_location()

            # If the snake eats an apple increase the eaten counter
            if head in self.apple_set:
                self.apple_set.remove(self.snake.get_head_location())
                self.increase_score_from_apple()
                self.eaten += 3

            if self.snake_head_hits_wall():
                self.finish_game()
                return


            wall_collision = self.snake_body_hits_wall_head()
            if wall_collision:
                self.handle_collision(wall_collision)

    def is_location_in_board(self, location: Location) -> bool:
        """Checks whether a given location is within the boundaries of the boar"""
        return not (location < Location(0, 0) or location > self.board_limit)

    def draw_board(self, gd: GameDisplay) -> None:
        if not self.debug:
            for loc in self.snake.get_entire_snake():
                print(loc)
                gd.draw_cell(loc.col, loc.row, "black")
        for loc in self.apple_set:
            gd.draw_cell(loc.col, loc.row, "green")
        for wall in self.wall_list:
            for loc in {loc for loc in wall.get_locations() if self.is_location_in_board(loc)}:
                gd.draw_cell(loc.col, loc.row, "blue")

    def get_score(self):
        return self.score_tracker.get_score()

    def end_round(self):
        self.round_manager.finish_round()

    def finish_game(self):
        """Finishes the game"""
        self.round_manager.finish_game()

    def is_over(self) -> bool:
        return self.round_manager.is_game_over()
