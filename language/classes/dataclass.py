# Acknowledgements____
# Tech with Tim
# Python Data Classes Are AMAZING! Here's Why
# https://www.youtube.com/watch?v=5mMpM8zK4pY&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=20&ab_channel=TechWithTim

from dataclasses import InitVar, dataclass, field
from typing import ClassVar, Optional

#
# This can be written in 4 lines of code
#


class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        x, y = self.x, self.y
        return f"Point({x=}, {y=})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


p1 = Point(1, 2)
p2 = Point(2, 1)
print(p1, p2)
print(p1 == p2)


#
# This fills in a bunch of methods that we would otherwise have to
# write. Added in version 3.7.
#

@dataclass
class PointDataClass:
    x: int
    y: int


p1 = PointDataClass(1, 2)
p2 = PointDataClass(2, 1)
print(p1, p2)
print(p1 == p2)
p1.x = 2
p1.y = 1
print(p1 == p2)


class InventoryItem:

    name: str
    unit_price: float
    quantity_on_hand: int = 0
    # field
    # 1. This is important to get a new list everytime, not a reference
    # to an existing list
    sizes: list[str] = field(default_factory=list)
    # 2. New list can be set to default values.
    # 3. init=Bool declares whether we want it to be included in the
    # initialization.
    sizes: list[str] = field(default=["medium"], init=False)
    # ClassVar # TODO
    # To declare class variables you need to give the type hint for
    # ClassVar from the typing import
    class_var: ClassVar[int] = 100

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand

    """
    This is done automatically for us
    """
    # def __init__(self, name: str, unit_price: float, quantity_on_hand: int):
    #     self.name = name
    #     self.unit_price = unit_price
    #     self.quantity_on_hand = quantity_on_hand


# Notice how we only store a reference to the list rather than a new
# list every time. This is solved by fields


print("Default mutable variables only store references")


def func(lst=[]):
    lst.append(1)
    print(lst)

# TODO: Review, also why do defaults work this way?


func()  # outputs: [1]
func()  # outputs: [1, 1]


print("Use Optional[TYPE] = None and then do a None check to assign")


def func(lst: Optional[list[str]] = None):
    if lst is None:
        lst = []
    lst.append(1)
    print(lst)


func()  # outputs: [1]
func()  # outputs: [1]

#
# Inheriting from a non-dataclass to a dataclass
#


class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width


@dataclass
class Square(Rectangle):
    # init automatically implements the wrapper, the repr, and the
    # equals method
    side: float

    # Then it calls the post_init dunder method
    def __post_init__(self):
        super().__init__(self.side, self.side)


#
# Inheriting from a dataclass to a dataclass
#

@dataclass
class Rectangle:
    width: int
    height: int


@dataclass
class ColoredRectangle(Rectangle):
    color: str


rect = ColoredRectangle(10, 10, "Green")


#
# Needing an initialization variable
#

@dataclass
class C:
    i: int
    j: int | None = None
    # InitVar will be included in the constructor, but not other methods
    # and also that it will be passed to post_init when it is called.
    database: InitVar[str | None] = None

    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')


c = C(10, database={"j": "j-value"})
