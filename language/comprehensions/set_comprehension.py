# Acknowledgements____
# Tech with Tim
# 10 Python Comprehensions You SHOULD Be Using
# https://www.youtube.com/watch?v=twxE0dEp3qQ&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=2&ab_channel=TechWithTim


# TODO: Review
print(
    "Remove duplicates from a list while squaring the values:\n{x**2 for x in nums}")
print(nums := [1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4])
unique_squares = {x**2 for x in nums}
print(unique_squares)
