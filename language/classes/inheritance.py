""" 
In this file we cover:
- Inheritance
- Abstract classes
- Interfaces

An abstract class is a class that cannot be instantiated on its own;
meant to be subclasses. They can contain abstract methods, which are 
declares but have no implementation. 

The benefits of these are:
1. Prevents instantiation of the class itself
2. Requires children to use inherited abstract methods

While there is a conceptual difference between abstract classes and 
interfaces in python. Python does not strictly deliniate between the
two. Instead They both use the abc import to do functionally the same 
thing.

What is the difference?
An abstract class:
1. Can define abstract methods (methods with no implementation)
2. Can also include concrete methods (with logic)
3. Can include attributes (both concrete or abstract)
4. Cannot be instantiaed directly
5. Is defined using abc.ABC and @abstractmethod

An interface:
1. Only defined abstract methods
2. No implementation, no attributes, no logic: only a contract
3. Enforced using ABC and only @abstractmethods

These classes can be extended using single, multiple, or mixin
inheritance.

Single:
- A class ingerits from one base class
"""
from abc import ABC, abstractmethod


class Animal:
    def eat(self):
        print("Eating")


class Dog(Animal):
    def bark(self):
        print("Barking")


"""
Multiple
- A class inherits from multiple base classes
"""


class CanFly:
    def fly(self):
        print("Flying")


class CanSwim:
    def swim(self):
        print("Swimming")


class Duck(CanFly, CanSwim):
    pass


"""
Mixin
- A mixin class is meant to be inherited from only to provide additional
functionality. not as a standalone parent.
"""


class LoggerMixin:
    def log(self, message):
        print(f"[LOG] {message}")


class Service(LoggerMixin):
    def run(self):
        self.log("Service is running")


# abc stands for abstract base class


class Vehicle(ABC):

    @abstractmethod
    def go(self):
        ...  # pass

    @abstractmethod
    def stop(self):
        ...  # pass


try:
    vehicle = Vehicle()
except TypeError as e:
    print(e)


class Car_no_inheritance(Vehicle):
    ...  # pass


try:
    car = Car_no_inheritance()
except TypeError as e:
    print(e)


class Car(Vehicle):

    def go(self):
        print("Drive the car")

    def stop(self):
        print("Stop the car")


car = Car()
car.go()
car.stop()


class Motorcycle(Vehicle):

    def go(self):
        print("Ride the motorcycle")

    def stop(self):
        print("Stop the motorcycle")


motorcycle = Motorcycle()
motorcycle.go()
motorcycle.stop()


"""
You must create every single abstract method!!
"""


class Boat(Vehicle):

    def go(self):
        print("Sail the board")


try:
    boat = Boat()
except TypeError as e:
    print(e)
