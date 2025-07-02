# # Make your code easier to adapt using Generics
# # Since 3.12 they've been updated to a newer syntax
# # This file is going over Python using that new syntax
# # to parameterize a type and retaining the advantage of
# # type checking.

# # TODO: Figure out how typing worked in Python 3.9

# from typing import Literal, Optional

# # Now if you create a Stack with type int it will expect ints for
# # all of the inputs.


# class Stack[T]:

#     def __init__(self) -> None:
#         self._container: list[T] = []

#     def __str__(self) -> str:
#         return str(self._container)

#     def push(self, item: T) -> None:
#         self._container.append(item)

#     def pop(self) -> T:
#         return self._container.pop()

#     def peek(self) -> Optional[T]:
#         if self.is_empty():
#             return None
#         return self._container[-1]

#     def is_empty(self) -> bool:
#         return self._container == []

#     def size(self) -> int:
#         return len(self._container)


# class NumericStack[T: (int, float)](Stack[T]):
#     """Generic type T mapped to and inheriting from the Stack."""

#     def __getitem__(self, index: int) -> T:
#         return self._container[index]

#     def __setitem__(self, index: int, value: T) -> None:
#         if 0 <= index < len(self._container):
#             self._container[index] = value
#         else:
#             raise IndexError("Stack index is out of range")

#     def sum(self) -> T | Literal[0]:
#         return sum(self._container)

#     def average(self) -> float:
#         if self.is_empty():
#             return 0
#         total: T | Literal[0] = self.sum()
#         return total / self.size()


# def main() -> None:
#     stack = Stack[int]()
#     stack.push(1)
#     stack.push(1.0)  # NOTICE: Types are not strictly enforced.
#     stack.pop()
#     print(f"Stack of ints: {stack}")
#     stack = Stack[float]()
#     stack.push(1.0)
#     print(f"Stack of floats: {stack}")
#     # Notice type violations will not produce an error.
#     # Static code analysis is your friend here.
#     numeric_stack = NumericStack[str]()
#     numeric_stack.push(1)
#     numeric_stack.push(10)
#     print(numeric_stack.average())
#     print(f"Vector of ints: {numeric_stack}")


# if __name__ == "__main__":
#     main()
