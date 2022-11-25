def print_seq(n, m):
    for i in [str(i) if i != m else str(i) + "!" for i in range(1, n + 1)]: print(i)


def print_seq(n):
    print(", ".join([str(i) for i in range(1, n + 1)]))


def is_prime_slow(n):
    return not bool(sum([1 if n % i == 0 else 0 for i in range(2, n)])) and n != 1


def is_prime_fast(n):
    return not bool(sum([1 if n % i == 0 else 0 for i in range(2, n // 2)])) and n != 1


def is_prime_very_fast(n):
    return not bool(sum([1 if n % i == 0 else 0 for i in range(3, n // 2, 2)])) and n != 1 and (n == 2 or n % 2 != 0)


def factorial_list(n):
    return [list(range(1, i)) for i in range(2, n + 2)]


def find_biggest(lst):
    return [lst[i] for i in range(len([sum(ls) for ls in lst])) if sum(lst[i]) == max([sum(ls) for ls in lst])][0]


print(find_biggest([[1, 2, 3], [10, -2], [1, 1, 1, 1]]))