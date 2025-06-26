# Acknowledgements____
# Tech with Tim
# Python Typing - Type Hints & Annotations
# https://www.youtube.com/watch?v=QORvB-_mbZ0&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=21&ab_channel=TechWithTim


# Reasons to do type annotations
# 1. Documentation
# 2. Better autocomplete
# 3. Other developers can read code easier
# 4. Static code analysis tools will tell you if you have type mismatchs

# x can store whatever type and be overwritten to any type
# unlike other languages: int x = 1
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, TypeVar


x = 1
x = "Thomas"

# Does not enforce that x should be a string, does not trigger an error.
# You need to use a static code analysis tool for this
# pip install mypy
# mypy [path-to-file]
# with this you can run static code analysis
x: str = 1

# parameter types       # return type


def add_numbers(a: int, b: int, c: int) -> int:
    return a + b + c


x: int = 0
x = add_numbers(1, 2, 3)
print(x)


# Need to import List on python 3.8 or below to use it as a
# subscriptable type.
list_of_lists: List[List[int]] = []

# Same for Dict
dict: Dict[str, str] = {"a": "b"}

hash_set: Set[int] = (1, 2,)


# Store a type within a variable
Vector = List[float]


def foo(v: Vector) -> Vector:
    pass


# foo()  # type this out to show type hints

Vectors = List[Vector]


def foo(v: Vectors) -> Vector:
    pass


# foo()  # type this out to show type hints

# Need to specify when types are Optional


def foo(output: Optional[bool] = False):
    pass


# foo()  # type this out to show type hints

# Declare this when you want to show you didn't just forget the type
# you actually want to show it can be anything.


def foo(output: Any):
    pass


# foo()  # type this out to show type hints


# Sequence says that anything that can be indexed is fine
def foo_seq(seq: Sequence[str]):
    if isinstance(seq, Sequence):
        for x in seq:
            print(x)
    else:
        print("Not a sequence")
    pass


foo_seq(['a', 'b', 'c'])
foo_seq(['a', 'b', 'c'])
foo_seq("hello")
foo_seq((i for i in range(100)))  # throws static code analysis error
foo_seq(1)  # throws static code analysis error


x: tuple = (1, 2, 3, "hello")
x: Tuple[int, int, int] = (1, 2, 3)  # Need to declare every index!!

#
# Callable[[parameter, types, go, here], return type]
#


def foo(func: Callable[[int, int], int]):
    func(1, 2)


def foo() -> Callable[[int, int], int]:
    func: Callable[[int, int], int] = lambda x, y: x + y
    return func

# TODO: Typing for lambdas

#
# Generics
#


# We don't know what type will be in the list, but it all must be the
# same type.

T = TypeVar('T')


def get_item(lst: List[T], index: int) -> T:
    return lst[index]


# TODO: Generic classes
