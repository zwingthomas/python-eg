# Acknowledgements____
# Tech with Tim
# Asyncio in Python - Full Tutorial
# https://www.youtube.com/watch?v=Qb9s3UiMSTA&t=208s&ab_channel=TechWithTim
#
# Corey Schafer
# Python Threading Tutorial: Run Code Concurrently Using the Threading Module
# https://www.youtube.com/watch?v=IEEhzQoKtQU&t=1381s&ab_channel=CoreySchafer

"""
How to select your asynchronous model?
1. asyncio for managing many waiting tasks
2. processes for maximizing preformance on cpu intensive tasks
3. threads for parallel tasks that share data with minimal cpu use

asyncio and threads are concurrency
processes are parrallelism

At the center of concurrency is the eventloop. The eventloop will allow
tasks to continue until they are waiting or in a stuck state. Then it
will move on to the next task and cycle through them until they are all
complete
"""

import time
import threading
from functools import wraps


def do_something(val: int = 1):
    print(f'Sleeping {val} second{"s" if val != 1 else ""}...')
    time.sleep(val)
    print(f'Done sleeping for {val} second{"s" if val != 1 else ""}')


def do_something_thread_executor(val: int = 1):
    print(f'Sleeping {val} second{"s" if val != 1 else ""}...')
    time.sleep(val)
    return f'Done sleeping for {val} second{"s" if val != 1 else ""}'


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        finish = time.perf_counter()
        print(f"Finished in {round(finish - start, 2)} seconds\n\n")
    return wrapper


@timer
def no_threads():
    do_something()  # This will take one second
    do_something()  # This will take another second


@timer
def old_threading():
    t1 = threading.Thread(target=do_something)
    t2 = threading.Thread(target=do_something)
    t1.start()  # This will take 1 second
    t2.start()  # This will run at the same time
    t1.join()
    t2.join()


@timer
def old_threading_for_loop():
    arr = []
    for _ in range(10):
        t = threading.Thread(target=do_something, args=[1.5])
        t.start()
        arr.append(t)
    for thread in arr:
        thread.join()


if __name__ == "__main__":
    no_threads()
    old_threading()
    old_threading_for_loop()
