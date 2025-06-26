from itertools import cycle


boolean = cycle([True, False])

for i in range(10):
    print(next(boolean))
