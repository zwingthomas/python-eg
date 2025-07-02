"""
Defines the **skeleton of an algorithm** in a base (abstract) class,
letting subclasses provide concrete implementations for one or more
steps. The template ensures the overall *sequence* stays unchanged.

Briefly,
- An abstract class declares **template_method()**—the high-level 
    workflow.
- Primitive operations are marked abstract; subclasses fill them in.
- Hook methods can provide optional extension points.

Example domain,
A *data-mining* pipeline: every source (CSV, JSON, API) must be  
**loaded → parsed → analysed → reported** in that order.  
Loading/parsing differ per source, but the rest is fixed.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from statistics import mean
from typing import List


class DataMiner(ABC):
    """The template defines the algorithm skeleton."""

    def mine(self) -> None:
        """The invariant high-level algorithm."""
        raw = self._extract()
        data = self._parse(raw)
        insights = self._analyze(data)
        self._report(insights)

    # --- primitive operations (must be supplied by subclasses) ---
    @abstractmethod
    def _extract(self) -> str: ...

    @abstractmethod
    def _parse(self, raw: str) -> List[float]: ...

    # --- invariant step shared by all concrete classes ---
    def _analyze(self, data: List[float]) -> float:
        """Default analysis: compute the average."""
        return mean(data)

    # --- hook method (optional override) ---
    def _report(self, result: float) -> None:
        print(f"Average = {result:.2f}")


# -----------------------------------------------------------------
# Concrete implementations
# -----------------------------------------------------------------
class CsvDataMiner(DataMiner):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _extract(self) -> str:
        with open(self.filepath) as fh:
            return fh.read()

    def _parse(self, raw: str) -> List[float]:
        return [float(x) for x in raw.strip().split(",")]


class InMemoryDataMiner(DataMiner):
    """Pretend we got numbers from an API call."""

    def __init__(self, payload: List[int]):
        self.payload = payload

    def _extract(self) -> str:
        # Simulate JSON-like comma-separated response
        return ",".join(map(str, self.payload))

    def _parse(self, raw: str) -> List[float]:
        # Apply an arbitrary transform for demo purposes
        return [float(x) * 1.5 for x in raw.split(",")]

    def _report(self, result: float) -> None:
        print(f"(API) weighted average → {result:.1f}")


# -----------------------------------------------------------------
# Demo
# -----------------------------------------------------------------
if __name__ == "__main__":
    # 1) CSV demo – write a sample file on the fly
    import tempfile
    import os

    with tempfile.NamedTemporaryFile("w+", delete=False) as fh:
        fh.write("10,20,30,40")
        path = fh.name

    CsvDataMiner(path).mine()
    os.unlink(path)

    # 2) In-memory demo
    InMemoryDataMiner([5, 15, 25, 35]).mine()
