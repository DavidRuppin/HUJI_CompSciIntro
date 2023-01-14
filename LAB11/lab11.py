#################################################################
# FILE : lab11.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex11 2022-2023
#################################################################

def cache(func):
    # Cache dict
    results = {}

    def inner(*args, **kwargs):
        nonlocal results
        hashable_args = str(args) + str(kwargs)

        if hashable_args not in results:
            results[hashable_args] = func(*args, **kwargs)
        return results[hashable_args]

    return inner


@cache
def add(a, b=1):
    return a + b

add(1)
add(2, 3)
add(4,b=4)