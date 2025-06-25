from datetime import date


class Calculator:
    def __init__(self, version: int):
        self.version = version

    def description(self):
        print(f'Currently running Calculator on version {self.version}')

    # Static methods don't rely on 'self'
    # They are kept in the class for organization
    # * in parameter allows input of any desired number of numbers. It
    # will be accessible now in the method as a tuple.
    @staticmethod
    def add_numbers(*numbers: float) -> float:
        return sum(numbers)


calc1 = Calculator(10)
calc2 = Calculator(12)
calc1.description()
calc2.description()
try:
    print(calc1.add_numbers(1, 2, 3, 4, 5))
except TypeError as e:
    print("Cannot call static methods on instances without the decorator.")
# Can call them on both with the decorator
print(Calculator.add_numbers(1, 2, 3, 4, 5))
