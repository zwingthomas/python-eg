"""
The problem this is trying to solve is when you need to create a copy
of an object. The issue with just creating a new one is that the 
object you want to copy may have gone through some state changes or 
there is other complexity with the object. The issue with simple copying
is that there are private/not visible fields. We also may only have
the interface of the object and not know exactly what we are dealing
with. Generic copying would also mean that we are tightly coupled to 
the object.

Prototypes allow:
- Lets you copy existing objects
- Without depending on their classes
- Only reliant on their classes
- The copied object must provide the copy functionality
- Useful in testing and pre-production

This functionality was given to us completely out of the box with
Python... as well as in most languages.
"""

from abc import ABC, abstractmethod
import copy


class Shape(ABC):
    @abstractmethod
    def draw(self):
        ...


class Square(Shape):
    def __init__(self, size):
        self.size = size

    def draw(self):
        print(f"Drawing a square of size {self.size}")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def draw(self):
        print(f"Drawing a circle of radius {self.radius}")


class AbstractArt:
    def __init__(self, bg_color, shapes):
        self.bg_color = bg_color
        self.shapes = shapes

    def draw(self):
        print(f"Background color is {self.bg_color}")
        [x.draw() for x in self.shapes]


if __name__ == "__main__":
    shapes = [Square(5), Square(3), Circle(8)]
    art1 = AbstractArt("red", shapes)
    # Only gives you references for mutable aspects
    art2 = copy.copy(art1)
    print(art1.draw() == art2.draw())
    # Gives you entirely new object with all the same values
    art2 = copy.deepcopy(art2)
    print(art1.draw() == art2.draw())
