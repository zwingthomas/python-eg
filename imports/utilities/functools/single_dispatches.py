from functools import singledispatch, singledispatchmethod

# Note: These only look at the first argument. To do more than the first
# argument, use type rich dataclasses or tuples.


@singledispatch
def handle_error(error):
    raise NotImplemented("Can't handle this error type")


@handle_error.register(TypeError)
def _(error):
    print("Handling TypeError")


@handle_error.register(AssertionError)
def _(error):
    print("Handling AssertionError")


@handle_error.register(ZeroDivisionError)
def _(error):
    print("Handling ZeroDivisionError")


try:
    i = 10 / 0
except Exception as e:
    handle_error(e)

try:
    i = -1
    assert i > 0
except Exception as e:
    handle_error(e)

try:
    raise TypeError
except Exception as e:
    handle_error(e)


class MyNum:
    def __init__(self, num):
        self.num = num

    @singledispatchmethod
    def add(self, num) -> Exception:
        return NotImplemented("Cannot add these two things!")

    @add.register(int)
    def _(self, num) -> int:
        self.num += num
        return self.num

    @add.register(str)
    def _(self, string) -> int:
        self.num += int(string)
        return self.num

    @add.register(list)
    def _(self, arr) -> int:
        for num in arr:
            self.add(num)
        return self.num


my_num = MyNum(0)
my_num.add(1)
my_num.add("100")
my_num.add([3, "2", 5])
print(my_num.num)
