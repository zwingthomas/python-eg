# Acknowledgements____
# mCoding
# What are Python __future__ imports?
# https://www.youtube.com/watch?v=7CRybttp0Uc&ab_channel=mCoding

"""
Future stores a bunch of other libraries and sets flags depending on
which import you use and then changes how it compiles your python
depending on which import you import. 

With future imports they will become a new feature in Python. However,
the features are not settled. They could even have breaking changes
before they are officially released.
"""

from __future__ import annotations


# type annotations
import typing


class Node:
    data: int


class Node2:
    data: Node2


class Node3:
    # Old solution: just put quotes around type annotations
    #               have to hope editor and static code analysis
    #               understand.
    data: "typing.Optional[Node3]"


print(Node.__annotations__)  # outputs: {'data': 'int'}
print(Node2.__annotations__)  # outputs: {'data': 'Node2'}


# Generator stop
def sub():
    yield 2
    return  # oops!
    yield 3


def gen():
    yield 1
    subgen = sub()
    yield next(subgen)
    yield next(subgen)  # Returns a StopIteration
    yield 4


try:
    for x in gen():
        print(x)
except RuntimeError as finished:  # NOTICE: THIS IS A RuntimeError
    print(finished)


def sub2():
    yield 2
    return  # oops!
    yield 3


def gen2():
    yield 1
    subgen = sub2()
    yield next(subgen)
    raise StopIteration  # Returns a StopIteration
    yield 4


try:
    for x in gen2():
        print(x)
except RuntimeError as finished:  # NOTICE: THIS IS A RuntimeError
    print(finished)

"""
It was not always like this. It used to be that the for loop would
silently terminate and just return less data. However, having a
StopIteration move outside of a generator is almost always an error so
it should be marked as a RuntimeError which is not handled by the 
for loop naturally like a regular StopIteration would be.
"""
