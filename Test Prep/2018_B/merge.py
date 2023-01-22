#################################################################

# FILE : Test Prep/2018_B_Q1

# WRITER : David Ruppin, ruppin, 322296336

# EXERCISE : intro2cs tests Test Prep/2018_B question Q1 2022-2023

#################################################################


def merge(word1, word2):
    merge_helper(word1, word2, '')


def merge_helper(word1, word2, combined):
    if not word1 and not word2:
        print(combined)

    if word1:
        merge_helper(word1[1:], word2, combined + word1[0])

    if word2:
        merge_helper(word1, word2[1:], combined + word2[0])


merge('abc', '12') # abc12 ab1c2 ab12c a1bc2 a1b2c a12bc 1abc2 1ab2c 1a2bc 12abc