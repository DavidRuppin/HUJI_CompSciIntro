import json
import re
from collections import namedtuple
from typing import NamedTuple, List


def load_json(filename):
    json_file = filename
    with open(json_file, 'r') as file:
        car_config = json.load(file)
    # now car_config is a dictionary equivalent to the JSON file
    return car_config


# HAD TO MOVE THESE TO GAME BECAUSE THE TESTS DON'T ALLOW FOR EXTRA FILES
class Location(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Location(self.row + other.row, self.col + other.col)

    def __eq__(self, other):
        try:
            return self.row == other[0] and self.col == other[1]
        except:
            return False


def create_command_regex_verifier(car_names: List[str], legal_moves: List[str]):
    REG_FORMAT = '[{}]\,[{}]'
    return re.compile(REG_FORMAT.format(''.join(car_names), ''.join(legal_moves)))