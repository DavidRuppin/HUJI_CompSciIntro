# ----------------------------------------------------#
# FILE : quadratic_equation.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex2 2023 
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES:
# ----------------------------------------------------#


def quadratic_equation(a, b, c):
    # Calculating the square root part
    sqrt_part = (b ** 2 - 4 * a * c) ** 0.5
    if type(sqrt_part) == complex or a == 0:
        return None

    # Getting the answers
    answers = {(-b + sqrt_part) / (2 * a), (-b - sqrt_part) / (2 * a)}
    if len(answers) > 1:
        return tuple(answers)
    else:
        return tuple(answers) + (None,)


def quadratic_equation_user_input():
    expression = input("Insert coefficients a, b, and c: ")
    a, b, c = [float(num) for num in expression.split(" ")]

    if a == 0:
        print("The parameter 'a' may not equal 0")
        return
    else:
        answers = quadratic_equation(a, b, c)
        if answers is None:
            print("The equation has no solutions")
        elif len(answers) == 2 and None not in answers:
            print("The equation has 2 solutions: {} and {}".format(*answers))
        else:
            print("The equation has 1 solution: {}".format(*answers))
