#################################################################
# FILE : iterator_question_1.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex 2022-2023
#################################################################

class MyMapIter:
    def __init__(self, func, *iterators):
        self.f = func
        self.iterators = iterators

    def __iter__(self):
        return iter(self)

    def __next__(self):
        args = [next(i) for i in self.iterators]
        return self.f(*args)

my_iter = MyMapIter(lambda x, y, z: [x, y, z], iter(range(5)), iter(range(3)), iter('abcd'))

class MyRange:
    def __iter__(self):
        for i in range(10):
            yield i


res = 1_000_000_000_00 in range(0, 1_000_000_000_01, 10)

i = 5
while i > 1:
    i
print(res)