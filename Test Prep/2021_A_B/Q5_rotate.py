#################################################################
# FILE : Q5_rotate.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest_2021_A_B 2022-2023
#################################################################


def rotate(s, d):
    x = s[:-(d % len(s))]
    y = s[-(d % len(s)):]
    return y + x

def test_rotate():
    assert rotate('abcde', 2) == 'deabc'
    assert rotate('asjdnjkasndjkas', 2) == 'asasjdnjkasndjk'
    assert rotate('asjdnjkasndjkas', len('asjdnjkasndjkas') + 1) == rotate('asjdnjkasndjkas', 1)


if __name__ == '__main__':
    test_rotate()