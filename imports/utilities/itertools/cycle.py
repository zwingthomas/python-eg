from itertools import cycle

# TODO: Add explanation

boolean = cycle([True, False])

for i in range(10):
    print(next(boolean))
