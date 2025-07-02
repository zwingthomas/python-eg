# Acknowledgements____
# Tech with Tim
# Asyncio in Python - Full Tutorial
# https://www.youtube.com/watch?v=Qb9s3UiMSTA&t=208s&ab_channel=TechWithTim

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

#TODO: Read this again
"""

import asyncio
import random

# A shared variable - we want to make sure no two coroutines are
# modifying this at the same time to avoid errors and unpredicable
# results.
shared_resource = 0

# An asyncio lock, only one coroutine can have the lock
lock = asyncio.Lock()

# An asyncio semaphore, the desired number of coroutines can have access
# at one time. In this case 4 coroutines can have access to the
# semaphore, which acts as a lock.
semaphore = asyncio.Semaphore(4)

# An asyncio event, this acts as a boolean flag to block off sections of
# code and wait till one part is done before executing them.
event = asyncio.Event()


#
# General async data processing
#
# Define a coroutine that simulates a time-consuming tsask


async def fetch_data(delay, id):
    print("Fetching data... id:", id)
    await asyncio.sleep(delay)  # Simulate an I/O intensive operation
    print("Data fetched! id:", id)
    return {"data": "some data", "id": id}

#
# Futures
#
# Typically used in lower level libraries, it is the promise of a future
# result. You're promising there will be a result in the future,
# although you do not know what it will be


async def set_future_result(future, value):
    await asyncio.sleep(2)
    future.set_result(random.randint(0, 10) * value)
    print(f"Set the future's result to {value}")

#
# Locks
#


async def modify_shared_resource():
    global shared_resource
    async with lock:
        # Critical section starts
        print(f"Resource before modification: {shared_resource}")
        shared_resource += 1
        await asyncio.sleep(1)
        print(f"Resource after modification: {shared_resource}")
        # Critical section ends

#
# Semaphores
#


async def access_resource(semaphore, resource_id):
    async with semaphore:
        # Simulate accessing a limited resource
        print(f"Accessing resource {resource_id}")
        await asyncio.sleep(1)  # simulate work with resource
        print(f"Releasing resource {resource_id}")

#
# Event
#


async def waiter(event):
    print("waiting for the event to be set")
    await event.wait()
    print("event has been set, continuing execution")


async def setter(event):
    await asyncio.sleep(2)
    event.set()
    print("event has been set!")


# Defines another coroutine that calls the other coroutines


async def main():  # -> Coroutine object:
    print("Start of main coroutine")

    # Not actually concurrent
    task1 = fetch_data(2, 1)
    task2 = fetch_data(2, 2)
    # Await the fetch_data coroutine, pausing execution of main until
    # fetch_data completes. A coroutine does not start running till it is
    # awaited. This these take 2 seconds each, 4 seconds in total.
    result1 = await task1
    print(f"Recieved result: {result1}")
    result2 = await task2
    print(f"Received result: {result2}")

    # Tasks
    # Now the program runs concurrently
    task3 = asyncio.create_task(fetch_data(2, 3))  # These will run
    task4 = asyncio.create_task(fetch_data(2, 4))  # at the same
    task5 = asyncio.create_task(fetch_data(2, 5))  # time!

    result3 = await task3   # It still does not run until it is awaited
    result4 = await task4
    result5 = await task5

    print(result3, result4, result5)

    # A quick way to concurrently run a bunch of coroutines. It will
    # automatically run all of these for us and gather them into a list.

    # Gather
    results = await asyncio.gather(
        fetch_data(2, 6),
        fetch_data(2, 7),
        fetch_data(2, 8)
    )

    for result in results:
        print(f"Recieved result: {result}")

    # A bad part of gather is that it is not good with error handling
    # It will not stop the other coroutines if one is it fail.
    # If you don't manually handle the possible exceptions you may get
    # a weird state in your program.

    # Below is a better approach, it automatically executes all the
    # tasks in the task group and then when they are all finished the
    # async with unblocks and the rest of the code runs.

    # TaskGroup
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for id, sleep_time in enumerate([9, 10, 11], start=1):
            task = tg.create_task(fetch_data(sleep_time, id))
            tasks.append(task)
    results = [task.result() for task in tasks]
    for result in results:
        print(f"Received result: {result}")

    # Future
    # TODO: Futures are weird, what can you do with them?
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    asyncio.create_task(set_future_result(future, random.randint(1, 10)))

    result = await future
    print(f"Received the future's result: {result}")

    # Locks
    # Kick off 5 tasks that modify a shared resource
    await asyncio.gather(*(modify_shared_resource() for _ in range(5)))

    # Semaphores
    # Kick off 20 tasks where four tasks will have access to the resource
    await asyncio.gather(*(access_resource(semaphore, i) for i in range(20)))

    # Event
    # It will run waiter only after setter kicks off the event
    # event acts as a boolean flag.
    await asyncio.gather(waiter(event), setter(event))

    print("End of main coroutine")

# Run the main coroutine object
# asyncio.run(...) awaits the return of the async function
asyncio.run(main())
