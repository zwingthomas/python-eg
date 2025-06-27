"""
Called either the decorator or the wrapper patern. It is very useful
and easy to understand. It allows us to modify the behavior of a 
function, method or a class that we do not fully have control over.

- Attach new behavior to an object
- Without altering existing code
- Overriding behavior
- Centralize functions

E.g.
Imagine you have a TCP/IP protocol that has a sendPacket() functionality.
This send packet functionality will not suffice as we want to communicate
with an API that we do not control. We could put a wrapper on top of this
In order to communicate between them. You could even go further and wrap
directly to the API service you want it to communicate to.

Lets implement this with a coffee shop as an example.

"""

from abc import ABC, abstractmethod


class CoffeeMachine(ABC):
    def make_small_coffee(self):
        ...

    def make_large_coffee(self):
        ...


class BasicCoffeeMachine(CoffeeMachine):
    # A base class
    def make_small_coffee(self):
        print("Basic coffee machine making small coffee")

    def make_large_coffee(self):
        print("Basic coffee machine making large coffee")

# We want to wrap this basic coffee machine in another layer that uses
# it and defines some new behavior


class EnhancedCoffeeMachine(CoffeeMachine):
    def __init__(self, basic_machine: BasicCoffeeMachine):
        self.basic_machine = basic_machine

    # Use the same functionality of the basic class
    def make_small_coffee(self):
        self.basic_machine.make_small_coffee()

    # Use a new functionality
    def make_large_coffee(self):
        print("Enhanced coffee machine: Making large coffee")

    # Added functionality, wrapping the basic functionality
    def make_milk_coffee(self):
        print("Enhanced coffee machine: Making milk coffee")
        self.basic_machine.make_small_coffee()
        print("Enhanced coffee machine: Adding milk")


if __name__ == "__main__":
    basic_machine = BasicCoffeeMachine()
    enhanced_machine = EnhancedCoffeeMachine(basic_machine)

    enhanced_machine.make_small_coffee()
    print()
    enhanced_machine.make_large_coffee()
    print()
    enhanced_machine.make_milk_coffee()
