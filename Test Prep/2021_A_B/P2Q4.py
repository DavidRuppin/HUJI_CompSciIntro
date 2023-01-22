#################################################################
from typing import Callable


# FILE : Test Prep/2021_A_B_Q4

# WRITER : David Ruppin, ruppin, 322296336

# EXERCISE : intro2cs tests Test Prep/2021_A_B question Q4 2022-2023

#################################################################

def outer(x: int):
    def inner(y: int) -> bool:
        return x + y > 23
    return inner

fluke: Callable[[int], Callable[[int], bool]] = outer
