# Acknowledgements____
# TutorialEdge
# Asyncio Synchronization Primitives Tutorial - Locks and Queues
# https://www.youtube.com/watch?v=kMcwcJdIvHI&ab_channel=TutorialEdge

"""
Notice that when run the queues take turns consuming from the producer.
Although the consumers sleep for two, they are ready to consume every
second because they can take turns who consumes each second! The 
sleep(2) does not change the functioning of this program at all!
"""


import asyncio
import random


async def producer(myQueue):
    while True:
        await asyncio.sleep(1)
        print("Putting new item onto queue")
        await myQueue.put(random.randint(1, 1000))


async def consumer(id, myQueue):
    while True:
        item = await myQueue.get()
        await asyncio.sleep(2)
        if item is None:
            break
        print("Consumer: {} consumered article with id: {}".format(id, item))


async def main():
    myQueue = asyncio.Queue(maxsize=10)
    await asyncio.gather(
        producer(myQueue),
        consumer(1, myQueue),
        consumer(2, myQueue)
    )

asyncio.run(main())
