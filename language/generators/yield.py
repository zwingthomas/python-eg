import collections
import math
import time
from typing import Iterator, NamedTuple


def get_values():
    yield "hello"
    yield "world"
    yield 123


try:
    gen = get_values()
    print(next(gen))  # outputs: hello
    print(next(gen))  # outputs: world
    print(next(gen))  # outputs: 123
    print(next(gen))  # StopIteration exception
except StopIteration as e:
    print("Handling StopIteration exception")


class Range:
    def __init__(self, stop: int):
        self.start = 0
        self.stop = stop

    def __iter__(self) -> Iterator[int]:
        curr = self.start
        while curr < self.stop:
            yield curr
            curr += 1


for x in Range(10):
    print(x)


# Files may be very large, so reading them in with generators rather
# than loading them into memory all at once is a very good idea.

class MyDataPoint(NamedTuple):
    x: float
    y: float
    z: float


def mydata_reader(file):
    for row in file:
        cols = row.rstrip().split(",")
        cols = [float(c) for c in cols]
        yield MyDataPoint._make(cols)


def example_reader():
    with open("mydata.txt", "r") as file:
        for row in mydata_reader(file):
            print(row)


example_reader()

# Generators are also helpful when you don't know when a process will
# end. Like finding the collatz reaching 1. It could be very long and
# you would not want to load all of that into memory at once.


def collatz(n):
    while True:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        yield n
        if n == 1:
            break


print(list(collatz(10024)))
# Get length without loading into memory
print(sum(1 for _ in collatz(10024)))


#
# You can also chain generators together:
# All of this is done lazily so all of this is done without loading
# the file into memory repeatedly.
# No need for more than one line at a time in memory!
#

with open("nums.txt", "r") as file:
    nums = (row.partition("#")[0].rstrip() for row in file)
    nums = (row for row in nums if row)
    nums = (float(row) for row in nums)
    nums = (x for x in nums if math.isfinite(x))
    nums = (max(0., x) for x in nums)
    s = sum(nums)
    print(f"The sum of the file is {s}")


#
# Generators are also bi-directional! You can send things into a
# generator. Notice this worker will go forever! This could be really
# powerful when using async and generators are essentially what the
# asyncio framework is built around.
#

def worker(f):
    tasks = collections.deque()
    value = None
    while True:
        batch = yield value
        value = None
        if batch is not None:
            tasks.extend(batch)
        else:
            if tasks:
                args = tasks.popleft()
                value = f(*args)
            # else:
            #    raise StopIteration


def producer():
    w = worker(str)
    w.send(None)
    w.send([(1,), (2,), (3,)])
    print(next(w))
    w.send([(4,)])
    w.send([(5,)])
    for output in w:
        print(output)
        time.sleep(2)


producer()
