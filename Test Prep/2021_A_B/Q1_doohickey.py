#################################################################
# FILE : Q1_doohickey.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest_2021_A_B 2022-2023
#################################################################

doohickey = lambda f: lambda *args, **kwargs: print('6')


@doohickey
def add(a, b):
    return a + b

add(5, 3)