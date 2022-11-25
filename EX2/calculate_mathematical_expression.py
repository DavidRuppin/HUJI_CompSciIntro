# ----------------------------------------------------#
# FILE : calculate_mathematical_expression.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex 2023 
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES:
# ----------------------------------------------------#

from typing import Union

ADD = "+"
SUB = "-"
MUL = "*"
DIV = ":"


def calculate_mathematical_expression(a: Union[int, float], b: Union[int, float], action: str) \
        -> Union[int, float, None]:
    # Checking every action, if none of them are valid return None
    if action == ADD:
        return a + b
    elif action == SUB:
        return a - b
    elif action == MUL:
        return a * b
    elif action == DIV:
        if b == 0:
            return None
        return a / b

    return None


def calculate_from_string(expression: str) -> Union[int, float, None]:
    # Iterating over the actions until a relevant one is found, returns None if no appropriate function was found
    for action in [ADD, SUB, MUL, DIV]:
        split_exp = expression.split(action)
        if len(split_exp) > 1:
            a, b = split_exp[0].strip(), split_exp[1].strip()
            return calculate_mathematical_expression(float(a), float(b), action)

    return None

assert calculate_from_string("10 : -2") == -5.0