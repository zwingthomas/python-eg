from functools import total_ordering

# Notice how total ordering has set us up for all comparative operations
# with only declaring two of them. Very nice and robust.


@total_ordering
class BadInt:
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        if isinstance(other, int | BadInt | str):
            return len(str(self.value)) == len(str(other))
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, int | BadInt | str):
            return len(str(self.value)) < len(str(other))
        return NotImplemented


my_int = BadInt("Five")

print(my_int <= 5)
print(my_int > 10)
print(my_int >= -10000)
print(my_int == 1000)
print(my_int == "five")
