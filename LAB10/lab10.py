#################################################################
# FILE : lab10.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex10 2022-2023
#################################################################

def to_curry(f):
    saved = []
    def inner(*args):
        return lambda args: f()

    return inner


if __name__ == '__main__':
    # to_curry(print)("Hello")("World!")()
    g = to_curry(lambda x, y, z: x + y * z)
    g1 = g(12)
    print(g1(1)(2)())
    print(g1(2)(3)())