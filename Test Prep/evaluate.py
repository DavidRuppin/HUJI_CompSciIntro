#################################################################
# FILE : evaluate.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs extest prep 2022-2023
#################################################################


initial_values = {'a': 5, 'b': 1}
program = [('c', (lambda x, y: x * y), 'a', 'a'),
           ('c', (lambda x, y, z: x + y + z), 'a', 'b', 'c'),
           ('return', 'c')]


def evaluate(prog, initial):
    for command in prog:
        if command[0] == 'return':
            return initial_values.get(command[1])

        f = command[1]
        initial_values[command[0]] = f(*[initial.get(arg) for arg in command[2:]])

assert evaluate(program, initial_values) == 31