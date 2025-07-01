# Acknowledgements
# NetworkChuck
# why are TUPLES even a thing?
# https://www.youtube.com/watch?v=fR_D_KIAYrE&ab_channel=NetworkChuck


"""
Python tuples are almost the same as lists. They are created with (,)
while lists are created with []. Why are there tuples if they are 
almost just the same as lists?

The key difference: Tuples are not mutable, they are immutable.
                    They cannot be changed after creation.

Changing a tuple will create an error, while lists can be changed.

This turns out to actually be very important. The fact they're 
immutable makes them substantially faster to create and work with.
"""

import timeit
import time

# LIST GEN SPEED: 2.92 seconds
print("List creation time:", timeit.timeit(
    stmt='["red", "blue", 5, 7, 12, 17, "Thomas"]', number=100000000))
# TUPLE GEN SPEED: 0.42 seconds
print("Tuple creation time:", timeit.timeit(
    stmt='("red", "blue", 5, 7, 12, 17, "Thomas")', number=100000000))

# Because lists are mutable, they are actually stored in two blocks
# of memory to allow for new and changing data.


"""
What is the use case though? When are we going to use data that can't 
be changed?

In lists you want to store homogenous data, data that is all the same
type and that you might change or update.

In tuples you want to store heterogenous data, data that is all 
different, but pertains to the same type of data.

Tuples are often the return type, especially for fetch calls.

They're also really good for "unpacking" which makes them great to use
in order to return a single variable and be able to unpack this on one
line. You can do this with lists, but it is less common to see.
"""


def ret_tuple(a, b, c):
    t = (a, b, c)
    return t


def ret_list(a, b, c):
    l = [a, b, c]
    return l


start = time.perf_counter()
for _ in range(10000000):
    a, b, c = ret_tuple("a", "b", "c")
end = time.perf_counter()
print(f"Tuple return time is {round(end - start, 3)} seconds: {a}, {b}, {c}")

start = time.perf_counter()
for _ in range(10000000):
    a, b, c = ret_list("a", "b", "c")
end = time.perf_counter()
print(f"List return time is {round(end - start, 3)} seconds: {a}, {b}, {c}")


"""
You don't actually need parathesis to make a tuple!
"""
totally_a_tuple = 1,
print(totally_a_tuple, type(totally_a_tuple))
totally_a_tuple = 1, 2, 4, 5
print(totally_a_tuple, type(totally_a_tuple))
