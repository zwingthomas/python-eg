# Acknowledgements____
# Tech with Tim
# 10 Python Comprehensions You SHOULD Be Using
# https://www.youtube.com/watch?v=twxE0dEp3qQ&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=2&ab_channel=TechWithTim

from itertools import count

cnt = count()  # See imports/itertools/count.py for more info

sum_of_squares = (x**2 for x in cnt)

while (x := next(sum_of_squares)) < 100000:
    print(x)
