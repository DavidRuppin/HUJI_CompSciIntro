# ----------------------------------------------------#
# FILE : temperature.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex2 2023 
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES:
# ----------------------------------------------------#

def is_vormir_safe(max_temp, temp1, temp2, temp3):
    # Summing the days when the temperature was too high. If it's 2 or more days, return True. Else return False
    return True if sum(1 for i in [temp1, temp2, temp3] if i > max_temp) >= 2 else False
