# ----------------------------------------------------#
# FILE : shapes.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex2 2023 
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES:
# ----------------------------------------------------#
from math import pi
from typing import Union


def shape_area() -> Union[int, float]:
    decision = input("Choose shape (1=circle, 2=rectangle, 3=triangle): ")
    # Quitting if the user's choice is invalid
    if decision not in ["1", "2", "3"]:
        return None

    if decision == "1":
        return calculate_circle_area(float(input()))
    elif decision == "2":
        params = float(input()), float(input())
        return calculate_rectangle_area(*params)
    elif decision == "3":
        return calculate_triangle_area(float(input()))


def calculate_circle_area(radius):
    return pi * (radius ** 2)


def calculate_rectangle_area(width, height):
    return width * height


def calculate_triangle_area(side):
    return (3 ** 0.5) * (side ** 2) / 4
