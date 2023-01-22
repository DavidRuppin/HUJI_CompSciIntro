#################################################################
# FILE : max_recursion_decorator.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest 2022-2023
#################################################################

def depth_check(f):
    current_depth, max_depth = 0, 0
    def inner(*args, **kwargs):
        nonlocal current_depth, max_depth
        current_depth += 1
        max_depth = max(current_depth, max_depth)
        res = f(*args, **kwargs)
        current_depth -= 1
        if current_depth == 0:
            return res, max_depth
        return res

    return inner



@depth_check
def fib(n):
    if n <= 1:
        return 1

    return fib(n - 1) + fib(n - 2)


print(fib(7))