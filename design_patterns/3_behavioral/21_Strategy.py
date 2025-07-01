"""
A *family of algorithms* is defined, encapsulated individually, and made
interchangeable at runtime.  The client picks a strategy object rather
than hard-coding the implementation.

Briefly,
- **Context** delegates work to a **Strategy** interface.
- Concrete strategy classes implement the same method in different ways.
- Behaviour can swap on the fly without touching the context’s code.

Example domain,
Imagine an analytics tool that occasionally needs to sort datasets of
varying size.  For tiny lists a simple bubble-sort may outperform the
setup cost of quick-sort; for large lists we want Python’s built-in
Timsort (`sorted`).  With the Strategy pattern the caller chooses—or an
autotuner chooses—the best algorithm.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint
from typing import List


# ---------------------------------------------------------------------------
# Strategy Interface
# ---------------------------------------------------------------------------
class SortStrategy(ABC):
    """All concrete strategies expose the *same* API."""

    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass


# ---------------------------------------------------------------------------
# Concrete Strategies
# ---------------------------------------------------------------------------
class BubbleSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        arr = data[:]
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        """Leverage Python’s highly optimised built-in sort."""
        return sorted(data)


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------
class DataSorter:
    """Holds a reference to a strategy; delegates the work."""

    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        return self._strategy.sort(data)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Generate random data
    data_small = [randint(0, 99) for _ in range(10)]
    data_large = [randint(0, 99) for _ in range(40)]

    sorter = DataSorter(BubbleSortStrategy())
    print("Bubble-sorted small:", sorter.sort(data_small))

    # Swap algorithm at runtime
    sorter.set_strategy(QuickSortStrategy())
    print("Quick-sorted large:", sorter.sort(data_large))
