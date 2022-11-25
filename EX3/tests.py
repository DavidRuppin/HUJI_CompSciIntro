from ex3 import *

########################
#                     A. 2                     #
########################

assert inner_product([1, 2, 3], [1, 2, 3]) == 14
assert inner_product([1, 2, 3], [10.5, -2, 0]) == 6.5
assert inner_product([1, 2, 3], []) is None
assert inner_product([0], [0]) == 0
assert inner_product([-10], [-5]) == 50
assert inner_product([], [1]) is None
assert inner_product([], []) == 0

########################
#                     A. 3                     #
########################

assert (sequence_monotonicity([1, 2, 3, 4, 5, 6, 7, 8])
        == [True, True, False, False])

assert (sequence_monotonicity([1, 2, 2, 3])
        == [True, False, False, False])

assert (sequence_monotonicity([1, 1, 1, 1])
        == [True, False, True, False])

assert (sequence_monotonicity([3, 2, 1, 1])
        == [False, False, True, False])

assert (sequence_monotonicity([7.5, 4, 3.141, 0.111])
        == [False, False, True, True])

assert (sequence_monotonicity([1, 0, -1, 1])
        == [False, False, False, False])

assert (sequence_monotonicity([])
        == [True, True, True, True])

assert (sequence_monotonicity([100])
        == [True, True, True, True])

assert (sequence_monotonicity([-10])
        == [True, True, True, True])

assert (sequence_monotonicity([0])
        == [True, True, True, True])

########################
#                     A. 4                     #
########################

bool_def = [True, True, False, False]
assert sequence_monotonicity(monotonicity_inverse(bool_def)) == bool_def

bool_def = [False, False, True, True]
assert sequence_monotonicity(monotonicity_inverse(bool_def)) == bool_def

bool_def = [True, False, True, False]
assert sequence_monotonicity(monotonicity_inverse(bool_def)) == bool_def

bool_def = [True, False, False, False]
assert sequence_monotonicity(monotonicity_inverse(bool_def)) == bool_def

bool_def = [False, False, True, False]
assert sequence_monotonicity(monotonicity_inverse(bool_def)) == bool_def

bool_def = [False, False, False, False]
assert sequence_monotonicity(monotonicity_inverse(bool_def)) == bool_def

bool_def = [False, True, False, False]
assert monotonicity_inverse(bool_def) is None

bool_def = [False, False, False, True]
assert monotonicity_inverse(bool_def) is None

bool_def = [True, True, True, True]
assert monotonicity_inverse(bool_def) is None

bool_def = [False, True, True, False]
assert monotonicity_inverse(bool_def) is None

bool_def = [True, False, False, True]
assert monotonicity_inverse(bool_def) is None

assert convolve([[1, 1, 1, 1, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 1], [
    0.5, 0, 0, 1, 0]]) == [[6, 5, 4], [3.5, 3, 3]]
assert convolve([[1, 1, 1, 1], [1, 0, 1, 0], [0, 0, 1, 0], [0.5, 0, 0, 1], [
    2, 0, 0, 0]]) == [[6.0, 5.0], [3.5, 3.0], [3.5, 2.0]]
assert convolve([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]) == [
    [9, 9], [9, 9]]
assert convolve([[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 0]]) == [[9], [8]]

########################
#                     A. 6                     #
########################

assert sum_of_vectors([[1, 1], [1, 3]]) == [2, 4]

assert sum_of_vectors([[1, 1, 1], [1, 0, 0], [0, 0, 100]]) == [2, 1, 101]

assert sum_of_vectors([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]) == [2, 2, 2, 2, 2]

assert sum_of_vectors([]) is None

########################
#                     A. 6                     #
########################

assert num_of_orthogonal([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3

assert num_of_orthogonal([[0, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3

assert num_of_orthogonal([[0, 0], [1, 2], [10, 5]]) == 2

assert num_of_orthogonal([[1, 1, 1, 1],
                          [2, 1, 3, 3],
                          [0, 0, 100, 33],
                          [8, 8, 8, 1.5],
                          [9, 9, 9, 9]]) == 0

assert num_of_orthogonal([[0], [0], [0], [0]]) == 6

print("All tests passed")
