# Acknowledgements____
# Bro Code
# Python method overriding 🙅
# https://www.youtube.com/watch?v=4Y83cUbDKZ8&ab_channel=BroCode


"""
Instances will use methods that more closely relate to their given 
object provided their method signatures match.
"""


class Animal:

    def eat(self):
        print("This animal is eating")


class Rabbit(Animal):
    ...


rabbit = Rabbit()
rabbit.eat()  # outputs: This animal is eating


"""
Override .eat()
"""


class Animal:

    def eat(self):
        print("This animal is eating")


class Rabbit(Animal):

    def eat(self):
        print("This rabbit is eating")


rabbit = Rabbit()
rabbit.eat()  # outputs: This rabbit is eating
