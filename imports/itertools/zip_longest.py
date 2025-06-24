from itertools import zip_longest

nums = [34, 25, 53, 646, 64]

print(list(zip_longest(range(10), nums)))
