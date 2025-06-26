""" 
An abstract class is a class that cannot be instantiated on its own;
meant to be subclasses. They can contain abstract methods, which are 
declares but have no implementation. 

The benefits of these are:
1. Prevents instantiation of the class itself
2. Requires children to use inherited abstract methods
"""

# abc stands for abstract base class
from abc import ABC, abstractmethod


class Vehicle(ABC):

    @abstractmethod
    def go(self):
        pass

    @abstractmethod
    def stop(self):
        pass


try:
    vehicle = Vehicle()
except TypeError as e:
    print(e)


class Car_no_inheritance(Vehicle):
    pass


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
You must inherit every single abstract method!!
"""


class Boat(Vehicle):

    def go(self):
        print("Sail the board")


try:
    boat = Boat()
except TypeError as e:
    print(e)
