#################################################################
# FILE : gen_str.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest 2022-2023
#################################################################


def gen_str(n: int):
    gen_str_helper(n, '')

def gen_str_helper(n, word):
    if n == 0:
        print(word)
        return
    for i in ('0','1'):
        if len(word) and word[-1] == '1' == i:
            continue
        gen_str_helper(n-1, word+i)


gen_str(3)