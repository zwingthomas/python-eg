from itertools import islice

# Combine arrays without storing the new array in memory
letters = ['a', 'b', 'c', 'd', 'e']
numbers = [0, 1, 2, 3]
names = ['Thomas', 'Letice']

print("Only end index - - - - - - -")

result = islice(range(10), 5)

for item in result:
    print(item)

print("Start index as well - - - - - - -")

result = islice(range(10), 2, 5)

for item in result:
    print(item)

print("Step - - - - - - -")

result = islice(range(10), 2, 5, 2)

for item in result:
    print(item)

print("Log file - - - - - - -")

with open('imports/itertools/test.log', 'r') as f:
    header = islice(f, 2)
    for line in header:
        print(line, end='')
