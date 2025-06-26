from functools import cache, cached_property, lru_cache
import random
import time


def maxsize_example() -> None:
    """
    lru_cache(maxsize=X)
    Notice how add_5 will only cache the 3 most recent values
    """
    @lru_cache(maxsize=3)
    def add_5(num: int) -> int:
        print(f"Adding 5 to {num}")
        return num + 5

    for i, x in enumerate([0, 1, 2, 0, 1, 2, 3, 4, 5, 0, 1, 2]):
        print(f"{i}: {add_5(x)}")


def fib_example() -> None:
    """
    maxsize efficiency
    Notice how even with a small cache size there can be massive
    improvements in the time taken to compute, especially recursive,
    functions.
    """
    def fib(n: int) -> int:
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    @lru_cache(maxsize=2)
    def cached_fib_2(n: int) -> int:
        if n <= 1:
            return n
        return cached_fib(n - 1) + cached_fib(n - 2)

    @lru_cache(maxsize=3)
    def cached_fib_3(n: int) -> int:
        if n <= 1:
            return n
        return cached_fib(n - 1) + cached_fib(n - 2)

    @cache  # Same as @lru_cache(maxsize=None)
    def cached_fib(n: int) -> int:
        if n <= 1:
            return n
        return cached_fib(n - 1) + cached_fib(n - 2)

    x = 40
    start = time.perf_counter()
    print(fib(x))
    print(f"Time without caching: {time.perf_counter() - start:.5f}")
    start = time.perf_counter()
    print(cached_fib_2(x))
    print(f"Time with caching two values: {time.perf_counter() - start:.5f}")
    start = time.perf_counter()
    print(cached_fib_3(x))
    print(f"Time with caching three values: {time.perf_counter() - start:.5f}")
    start = time.perf_counter()
    print(cached_fib_3(x))
    print(f"Time with unbound caching: {time.perf_counter() - start:.5f}")


class ToolShed():
    """
    A simple object to show how cache and cached_property work within a
    class
    """

    def __init__(self, size):
        self.size = size

    # For use with methods with parameters
    @cache
    def get_item_location(self, item: str) -> list[int]:
        # inclusive
        print("Item found!")
        return [random.randint(1, self.size), random.randint(1, self.size)]

    # For use with parameterless calculated or retrived attributes
    @cached_property
    def shed_location(self) -> int:
        print("Found shed!")
        return random.randint(1, self.size)

    def grab_item(self, item: str) -> None:
        print("Grabbing item.")
        return self.get_item_location(item=item)


def test_toolshed(size: int) -> None:
    shed = ToolShed(size)
    shed.grab_item(item="drill")
    shed.grab_item(item="screw driver")
    shed.grab_item(item="measuring tape")
    shed.grab_item(item="drill")
    shed.grab_item(item="screw driver")
    shed.grab_item(item="measuring tape")

    # Notice how we do not use () as this is not callable and is a
    # property. It will return the same no matter how many times we call
    # upon the property.
    for _ in range(10):
        print(f"Shed is located at: {shed.shed_location}")


if __name__ == "__main__":
    maxsize_example()
    fib_example()
    # Notice how cached properties differ between instances of the object
    test_toolshed(10)
    test_toolshed(100)
