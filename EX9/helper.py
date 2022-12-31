import json
from collections import namedtuple
from typing import NamedTuple


def load_json(filename):
    json_file = filename
    with open(json_file, 'r') as file:
        car_config = json.load(file)
    # now car_config is a dictionary equivalent to the JSON file
    return car_config


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

