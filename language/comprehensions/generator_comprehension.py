from itertools import count

cnt = count()  # See imports/itertools/count.py for more info

sum_of_squares = (x**2 for x in cnt)

while (x := next(sum_of_squares)) < 100000:
    print(x)
