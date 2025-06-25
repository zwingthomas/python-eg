from datetime import date
from typing import Self  # new in Python 3.11

#
# Class methods will affect the actual class
# Whereas instance methods affect an instance of the class
# And static methods do not operate on the class at all
#


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def description(self) -> str:
        return f'{self.name} is {self.age} years old.'

    @classmethod
    def age_from_year(cls, name: str, birth_year: int) -> Self:
        current_year: int = date.today().year
        age: int = current_year - birth_year
        return cls(name, age)


if __name__ == "__main__":
    thomas = Person.age_from_year('Thomas', 1997)
