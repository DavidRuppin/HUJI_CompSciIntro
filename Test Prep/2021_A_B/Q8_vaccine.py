#################################################################
# FILE : Q8_vaccine.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest 2022-2023
#################################################################

vaccine_total = 50

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.vacs = 0
        self.spouse = None

    def get_vac_num(self):
        return self.vacs

    def set_vac_num(self, n: int):
        self.vacs = n

    def get_age(self):
        return self.age

    def get_name(self) -> str:
        return self.name

    def marry(self, person):
        if self.spouse in [None, person] and person.spouse in [None, self]:
            self.spouse = person
            person.spouse = self
        else:
            raise Exception('Cant marry twice fool')

    def get_spouse(self):
        return self.spouse


class VaccinationCenter:
    def __init__(self, min_age: int):
        self.min_age = min_age

    def set_age_limit(self, new_min_age: int):
        self.min_age = new_min_age

    def give_vaccine(self, person):
            if self.is_eligible(person):
                global vaccine_total
                vaccine_total -= 1
                person.set_vac_num(person.get_vac_num() + 1)



    def is_eligible(self, person) -> bool:
        if vaccine_total <= 0:
            return False

        spouse_eligible = False

        if person.get_spouse():
            spouse_eligible = person.get_spouse().get_vac_num() > 0

        return person.get_age() >= self.min_age or person.get_vac_num() > 0 or spouse_eligible


def test_vaccine():
    vac_center = VaccinationCenter(25)

    A = Person('Dingus', 20)
    B = Person('Bingus', 27)
    C = Person('Meep', 23)

    assert vac_center.is_eligible(A) == False
    A.marry(B)
    assert vac_center.is_eligible(A) == False
    vac_center.give_vaccine(B)
    assert vac_center.is_eligible(A) == True
    vac_center.give_vaccine(A)
    assert A.get_vac_num() == 1
    B.marry(A)

    raised_exception = False
    try:
        B.marry(C)
    except:
        raised_exception = True

    assert raised_exception == True

def main():
    test_vaccine()