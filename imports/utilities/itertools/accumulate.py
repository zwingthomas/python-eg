from itertools import accumulate, repeat
import operator

# TODO: Add explanation

print("Accumulating by going over a list of ones with addition")
numbers = repeat(1, times=10)
result = accumulate(numbers)
for item in result:
    print(item)

print("Accumulating by going over a list of twos with multiplication")
numbers = repeat(2, times=10)
result = accumulate(numbers, operator.mul)
for item in result:
    print(item)
