from itertools import chain

# Combine arrays without storing the new array in memory
letters = ['a', 'b', 'c', 'd', 'e']
numbers = [0, 1, 2, 3]
names = ['Thomas', 'Letice']

combined = chain(letters, numbers, names)

for item in combined:
    print(item)
