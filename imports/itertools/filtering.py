from itertools import compress, filterfalse, dropwhile, takewhile


def lt_2(x):
    return x < 2


letters = ['a', 'b', 'c', 'd']
selectors = [True, True, False, True]
numbers = [0, 1, 2, 3, 4, 5, 0, 2, 1, 3, 4]

print("Compress with selectors - - - - - - -")

result = compress(letters, selectors)

for item in result:
    print(item)

print("Filter with method - - - - - - -")

result = filter(lt_2, numbers)

for item in result:
    print(item)

print("Filterfalse with same method - - - - - - -")

result = filterfalse(lt_2, numbers)

for item in result:
    print(item)

print("Dropwhile with same method - - - - - - -")

result = dropwhile(lt_2, numbers)

for item in result:
    print(item)

print("Takewhile with same method - - - - - - -")

result = takewhile(lt_2, numbers)

for item in result:
    print(item)
