#################################################################
# FILE : P2Q1_exceptions.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest_2021_A_B 2022-2023
#################################################################


lst1 = [(5, 2), 0, '-7', 4, 8]
lst2 = [1, 2, 3, 4, 5]

correct = 'aba1cf'

res = ''

try:
    for item in lst1:
        try:
            res += str(int(lst2[item-1] / item))
        except TypeError:
            res += 'a'
        except ZeroDivisionError:
            res += 'b'
        except IndexError:
            res += 'c'
except:
    res += 'e'
finally:
    res += 'f'

print(res)
assert res == correct

