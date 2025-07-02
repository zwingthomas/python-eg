# Acknowledgements____
# mCoding
# Python Generators
# https://www.youtube.com/watch?v=tmeKsb2Fras&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=6&ab_channel=mCoding

import collections
import time


def gen():
    # Shorter version
    yield from (x*x for x in range(5))
    # Longer version
    for sq in (x*x for x in range(5)):
        yield sq


# This is not the reason 'yield from' was introduced into Python though,
# it was introduced in order to faciliate the bi-directional nature
# of the Python language.

# TODO

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
            else:
                raise StopIteration


def quiet_worker(f):
    while True:
        w = worker(f)
        try:
            yield from w  # Returns the return value of the subgenerator
        except Exception as exc:
            print(f"Ignoring: {exc}")


def producer():
    w = quiet_worker(str)
    w.send(None)
    w.send([(1,), (2,), (3,)])
    print(next(w))
    w.send([(TypeError,)])
    w.send([(4,)])
    w.send([(5,)])
    for output in w:
        print(output)
        time.sleep(2)


producer()
