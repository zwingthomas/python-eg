from itertools import starmap, repeat

two = repeat(2)
squares = map(pow, range(10), two)
print(list(squares))
# Starmap takes a list of tuples into map instead of parameters
# TODO How is this powerful?
squares = starmap(pow, zip(range(10), two))
print(list(squares))

# TODO: Compare this with map, add explanation
