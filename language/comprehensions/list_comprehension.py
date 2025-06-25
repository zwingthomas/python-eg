import pprint

print("\nBasic list comprehension:\n[x for x in range(10)]")
print([x for x in range(10)])
print("\n")


print("Add one to everything in the list:\n[x + 1 for x in range(10)]")
print([x + 1 for x in range(10)])
print("\n")


print("Just the evens:\n[x for x in range(10) if x % 2 == 0]")
print([x for x in range(10) if x % 2 == 0])
print("\n")


print("Matching a variety of criteria: ")
print("""[
    string
    for string in options
    if len(string) >= 2
    if string[0] == 'a'
    if string[-1] == 'y'
]""")
print(options := ["any", "albany", "apple", "happy", "world", "hello", ""])
print([
    string
    for string in options
    if len(string) >= 2
    if 'a' in string
    and (string[0] == 'a' or string[-1] == 'y')
])
print("\n")


print(
    "Flattening a matrix (list of lists): [num for row in matrix for num in row]")
print(matrix := [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print([num for row in matrix for num in row])
print("\n")


print(
    "Categorizing numbers as even or odd:\n['Even' if x % 2 == 0 else 'Odd' for x in range(10)]")
print(['Even' if x % 2 == 0 else 'Odd' for x in range(10)])
print("\n")


print(
    "Building a 3D list:\n[[[num for num in range(5)] for _ in range(5)] for _ in range(5)]")
printer = pprint.PrettyPrinter()
printer.pprint([[[num for num in range(5)] for _ in range(5)]
               for _ in range(5)])
print("\n")


def square(x):
    return x ** 2


print("Using functions:\n[square(x) for x in range(10)]")
print([square(x) for x in range(10)])
print("\n")
