#################################################################
# FILE : hello_turtle.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex1 2023
# WEB PAGES I USED: https://docs.python.org/3/library/turtle.html
#################################################################

import turtle


def draw_triangle():
    for i in range(3):
        triangle_forward_and_turn()


def triangle_forward_and_turn():
    turtle.forward(45)
    turtle.right(120)


def draw_sail():
    turtle.left(90)
    turtle.forward(50)
    turtle.right(150)
    draw_triangle()
    turtle.right(30)
    turtle.penup()
    turtle.forward(50)
    turtle.pendown()
    turtle.left(90)


def draw_sails():
    for i in range(3):
        # preparing for the actual sail by moving forward
        turtle.forward(50)
        draw_sail()

    # moving to the end of the boat
    turtle.forward(50)


def draw_ship():
    # drawing the sails
    draw_sails()
    # drawing the body
    turtle.left(60)
    turtle.back(20)
    turtle.left(120)
    turtle.forward(180)
    turtle.left(120)
    turtle.back(20)


def draw_fleet():
    # first ship
    draw_ship()
    # moving to the beginning of the second ship
    turtle.setheading(0)
    turtle.penup()
    turtle.back(300)
    turtle.pendown()
    draw_ship()


if __name__ == '__main__':
    draw_fleet()
    turtle.done()
