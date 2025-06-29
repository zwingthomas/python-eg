# Acknowledgements____
# Programming and Math Tutorials
# Python Bisect Module tutorial | fast insertion into sorted lists


"""
bisect finds the insertion point for adding an item into a sorted list.
- It runs in O(log(n))
Remember inseting is still O(n)

This works for any object that can be sorted: even strings!

If you use this on an unsorted list you will get unpredictable results.
It will still try to put it in the right place and kind of get something
that's arguably correct. But keep in mind it does not throw an error 
if your list is not sorted and it does not sort your list.

Keep in mind this can give you returns that are larger than your list
if you are trying to find something greater than the maximum input.
"""
from dataclasses import dataclass
from typing import ClassVar
from itertools import count
from functools import total_ordering
from random import randint
import bisect


print("\nbisect_left______")
a = [24, 33, 41, 41, 45, 50, 53, 59, 59, 59, 62, 66, 70]
a_with_indexes = [(i, num) for i, num in zip(count(), a)]
print("Looking where to insert 54")
i = bisect.bisect_left(a, 54)
print("First number >= 54 at index: ", i)
print(a_with_indexes[i - 4: i + 5])
print("Inserting 54 three times")
a.insert(7, 54)
a.insert(7, 54)
a.insert(7, 54)
a_with_indexes = [(i, num) for i, num in zip(count(), a)]
i = bisect.bisect_left(a, 54)
print("54 found at index: ", i)
print(a_with_indexes[i - 4: i + 5])
print("bisect.bisect_left found the first item greater than or equal to 54")
print("Subtract 1 from this index to find the first element less than 54")


print("\nbisect_right______")
a = [24, 33, 41, 41, 45, 50, 53, 59, 59, 59, 62, 66, 70]
a_with_indexes = [(i, num) for i, num in zip(count(), a)]
print("Looking where to insert 54")
i = bisect.bisect_right(a, 54)
print("First number strictly > 54 at index: ", i)
print(a_with_indexes[i - 4: i + 5])
print("Inserting 54 three times")
a.insert(7, 54)
a.insert(7, 54)
a.insert(7, 54)
a_with_indexes = [(i, num) for i, num in zip(count(), a)]
i = bisect.bisect_right(a, 54)
print("Now the first number strictly > is at index: ", i)
print(a_with_indexes[i - 4: i + 5])
print("bisect.bisect_right found the first item greater than or equal to 54")
print("Subtract 1 from this index to find the first element less than 54")


"""
insort puts things directly into the list for us!
Now it is hard to tell what the difference between insort_left and 
insort_right is just with integers. As it will put the matches next
to one another. If there isn't a match it will put things in their
proper place and there is not a difference between these two.

But if there is a match, and you're using mutable type-rich objects, 
then you will see a very big difference between the two.

"""


@dataclass
@total_ordering
class asdf:
    cnt: ClassVar[int] = 0

    def __init__(self):
        type(self).cnt += 1
        self._value: int = randint(1, 100)
        self.string: str = chr((type(self).cnt + 65) % 127)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self):
        return f"({str(self._value)}, {self.string})"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, input):
        self._value = input


print("\ninsort_left______")
d = sorted([asdf() for _ in range(8)])
print([str(entry) for entry in d])
x = asdf()
x.value = d[4].value
print("Inserting new object with same sortable value as the 5th object with bisect.insort_left(list, obj):", x)
bisect.insort_left(d, x)
print([str(entry) for entry in d])
print("Notice how this object goes to the left of matches")

print("\ninsort_right______")
d = sorted([asdf() for _ in range(8)])
print([str(entry) for entry in d])
x = asdf()
x.value = d[4].value
print("Inserting new object with same sortable value as the 5th object with bisect.insort_right(list, obj):", x)
bisect.insort_right(d, x)
print([str(entry) for entry in d])
print("Notice how this object goes to the right of matches")


print("")
