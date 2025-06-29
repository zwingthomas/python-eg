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

start = time.perf_counter()


def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done sleeping')


do_something()

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} seconds")
