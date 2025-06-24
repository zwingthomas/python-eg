from itertools import count


# Generates an dynamic iterator for you

counter = count()

for x in range(10):
    if x % 2 == 0:
        next(counter)
print(counter)


# Helpful for enumeration

counter = count()
arr = [34, 25, 65, 76, 87]
print(list(zip(counter, arr)))


# Can pass arguments for (Start, Increment)

counter = count(start=5, step=2.5)
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))

# Note count is an iterable, TODO how to get the value at a given time?
