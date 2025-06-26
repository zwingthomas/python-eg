# Acknowledgements____
# mCoding
# Watch out for this (async) generator cleanup pitfall in Python
# https://www.youtube.com/watch?v=N56Jrqc7SBk&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=15&ab_channel=mCoding

import asyncio
import contextlib


class Resource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"cleanup: {self.name}")


def gen():
    with Resource("database/lock/file/etc."):
        for x in range(3):
            print(f"yield {x}")
            yield x


async def gen2():
    with Resource("database/lock/file/etc."):
        for x in range(3):
            print(f"yield {x}")
            yield x


def main():
    for x in gen():
        print(f"got {x}")
    print("after loop")


def main2():
    for x in gen():
        print(f"got {x}")
        if x == 1:
            break
    print("after loop")


def main3():
    g = gen()
    for x in g:
        print(f"got {x}")
        if x == 1:
            break
    print("after loop")


def main4():
    g = gen()
    for x in g:
        print(f"got {x}")
        if x == 1:
            raise Exception
    g.close()
    print("after loop")


def main5():
    with contextlib.closing(gen()) as g:
        for x in g:
            print(f"got {x}")
            if x == 1:
                break
    print("after loop")


async def main6():
    with Resource("outer resource"):
        async for x in gen2():
            print(f"got {x}")
            if x == 1:
                break
        print("after loop")


async def main7():
    with Resource("outer resource"):
        async with contextlib.aclosing(gen2()) as g:
            async for x in g:
                print(f"got {x}")
                if x == 1:
                    break
            print("after loop")


if __name__ == "__main__":
    print("Full run of generator:")
    main()
    print("Notice the order of our messages, generator cleans up prior to the loop terminating.")

    print("\nBreak outside generator:")
    main2()  # breaking outside of our generator
    print("Notice we still clean up first even though we terminated the generator. This is possible because when a generator is garbage collected it automatically has its garbage collector called.")

    print("\nPull the generator into the context of the main function not only the for loop.")
    main3()
    print("Now garbage collection happens after the main function terminates. This could already be an issue if it we were holding a lock and stuff afterwords in the main function needed the lock. Inner resources are not always cleaned up before inner resourced in Python.")

    print("\nCould we manually close it?")
    try:
        main4()
    except Exception:
        print("No! What if there is an exception thrown?")

    print("\nYou must use contextlib.closing(gen()) as g to wrap generators instead of just holding onto their reference:")
    main5()
    print("You typically just see people ignoring this. They don't use shared resources and don't hold on to a reference for a generator. However, if you are using async generators the problem is significantly worse.")

    print("\nLet's try with async generators:")
    asyncio.run(main6())
    print("Now the outer resource is cleaned up before the inner one! An async generator is async, but the garbage collector is not. The best it can do is to schedule the task to be closed, but it cannot await for this.")

    print("\nTo solve this surround any async for loops that use a generator with async with contextlib.aclosing(gen2()) as g:")
    asyncio.run(main7())

    # This is nonsense, there is a PEP, PEP 533, that proposes an __aiterclose__ magic method that would solve this for us. Right now there is no better solution.
