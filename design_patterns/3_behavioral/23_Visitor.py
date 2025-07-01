"""
Separates an **algorithm** from the objects on which it operates, so you
can add new operations without modifying the object structure.

Briefly,
- **Element** classes accept a visitor via `accept(self, visitor)`.
- **Visitor** hierarchy implements a `visit_X()` method for each element
  type.
- Adding a new *visitor* adds behaviour; adding a new *element* still
  requires touching visitors, so pick this pattern when element classes
  are stable but operations change.

Example domain,
An expression tree with literals and binary operators.  We'll build two
visitors:
1. **Evaluator** - compute the numerical result.
2. **Printer**   - pretty-print as infix notation.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol

# ---------------------------------------------------------------------------
# Visitor Interface
# ---------------------------------------------------------------------------


class Visitor(Protocol):
    def visit_number(self, element: "Number") -> float: ...
    def visit_add(self, element: "Add") -> float: ...
    def visit_multiply(self, element: "Multiply") -> float: ...


# ---------------------------------------------------------------------------
# Element hierarchy
# ---------------------------------------------------------------------------
class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


class Number(Expr):
    def __init__(self, value: float):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_number(self)


class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right


class Add(BinaryExpr):
    def accept(self, visitor: Visitor):
        return visitor.visit_add(self)


class Multiply(BinaryExpr):
    def accept(self, visitor: Visitor):
        return visitor.visit_multiply(self)


# ---------------------------------------------------------------------------
# Concrete Visitors
# ---------------------------------------------------------------------------
class EvaluateVisitor:
    def visit_number(self, element: Number):
        return element.value

    def visit_add(self, element: Add):
        return element.left.accept(self) + element.right.accept(self)

    def visit_multiply(self, element: Multiply):
        return element.left.accept(self) * element.right.accept(self)


class PrintVisitor:
    def visit_number(self, element: Number):
        return str(element.value)

    def visit_add(self, element: Add):
        return f"({element.left.accept(self)} + {element.right.accept(self)})"

    def visit_multiply(self, element: Multiply):
        return f"({element.left.accept(self)} * {element.right.accept(self)})"


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Build expression: (5 + 3) * 2  → should evaluate to 16
    expr = Multiply(Add(Number(5), Number(3)), Number(2))

    evaluator = EvaluateVisitor()
    printer = PrintVisitor()

    print("Expression :", printer.visit_multiply(expr))
    print("Evaluates to:", evaluator.visit_multiply(expr))
