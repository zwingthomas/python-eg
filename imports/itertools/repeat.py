from itertools import repeat

counter = repeat(2, times=3)

while counter:
    try:
        print(next(counter))
    except StopIteration as end:
        print("Done!")
        break


for square in map(pow, range(10), repeat(2)):
    print(square)
