"""
Python does not have strict access modifiers like private, protected,
or public from languages like Java or C++. But it uses naming
conventions to signal access levels:

public_name - public, accessible from anywhere within scope
_protected  - protected, meant for internal use (not enforced)
__private   - private, name-mangled to prevent accidental access

Thus encapsulation is the concept of bundling data and methods that
operate together within a single unit, normally a class, and restricting
direct access to some of the object's internal components. With a goal
of enforcing data hiding, ensuring internal representation is sheilded
from the outside, and only accessed through a controlled interface.

The benefits and applications are as follows:
1. Control access to data
2. Only allow safe operations
3. Prevent misuse or bugs
4. Maintainability - you can change the internal implementation without 
                     affecting external code.

You can still access the private attributes, but never should. Python
makes this intentionally difficult. It is done by:
account = BankAccount("Alice", 1000)
print(account._BankAccount__pin)

This Python only has encapsulation by concention, not strict
enforcement.
"""


class Person:

    def __init__(self, name, age, gender):
        self.__name = name      # set to private with __
        self.__age = age        # set to private with __
        self.__gender = gender  # set to private with __

    @property
    def Name(self):
        return self.__name

    @Name.setter
    # Usually this would not work as method overloading is not a feature
    # of Python. Our decorators allow us to do this.
    def Name(self, value):
        # Normally people would be able to directly assign to self.name
        # if you dont want direct access you must use getters and
        # setters. This gives you more control over your class.
        if isinstance(value, str):
            if value == "Tom":
                self.__name = "Thomas"
            else:
                self.__name = value
        else:
            raise TypeError("Name must be a string.")

    @staticmethod
    def greeter():  # static method does not pass self
        print("Hello, create a person!")


p1 = Person("Thomas", 27, 'm')
print(p1.Name)
try:
    print(p1.__name)
except AttributeError as e:
    print(e)
# Attributes can still be directly accessed, but never should be
print(p1._Person__name)
Person.greeter()    # These output
p1.greeter()        # the same thing
