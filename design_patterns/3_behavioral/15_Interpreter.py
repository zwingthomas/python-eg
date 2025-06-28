"""
An interpreter allows you to understand a language given to the 
computer and understand the system or expression. It does this by
building a tree with the language given to it. Think about a computer
running the order or operations with a mathematical expression given 
to it. This has a lot of applications.

Briefly
- Recursively evaluate grammar and expressions
- Parsing, processing engines, etc.
- Two components
    - Terminal expression (in a mathematical formula this is the numbers)
    - Non-terminal expressions (this would be operations)

"""


class AbstractExpression():
    @staticmethod
    def interpret():
        pass


class Number(AbstractExpression):
    """ Terminal expression """

    def __init__(self, value: int | float):
        self.value = float(value)

    def interpret(self):
        return self.value


class AlgebraExpression(AbstractExpression):
    """ Non-terminal expression """

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(AlgebraExpression):
    def interpret(self):
        return self.left.interpret() + self.right.interpret()


class Subtract(AlgebraExpression):
    def interpret(self):
        return self.left.interpret() - self.right.interpret()


class Multiply(AlgebraExpression):
    def interpret(self):
        return self.left.interpret() * self.right.interpret()


class Divide(AlgebraExpression):
    def interpret(self):
        return self.left.interpret() / self.right.interpret()


if __name__ == "__main__":
    target = "-11.37 + 5 - 2 * 7 / 5 + 11"
    tokens = target.split(" ")
    expressions = []
    for i in range(len(tokens)):
        if i == 0:
            expressions.append(Number(tokens[i]))
        elif tokens[i] == '+':
            expressions.append(Add(expressions.pop(), Number(tokens[i + 1])))
        elif tokens[i] == '-':
            expressions.append(
                Subtract(expressions.pop(), Number(tokens[i + 1])))
        elif tokens[i] == '*':
            expressions.append(
                Multiply(expressions.pop(), Number(tokens[i + 1])))
        elif tokens[i] == '/':
            expressions.append(
                Divide(expressions.pop(), Number(tokens[i + 1])))

    # Note: this does not follow order of operations
    print(expressions.pop().interpret())
