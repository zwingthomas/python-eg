
print(
    "Remove duplicates from a list while squaring the values:\n{x**2 for x in nums}")
print(nums := [1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4])
unique_squares = {x**2 for x in nums}
print(unique_squares)
