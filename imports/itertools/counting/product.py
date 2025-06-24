from itertools import product


# All the ways to group items where order does matter and there can be
# repeats
letters = ['a', 'b', 'c', 'd', 'e']
numbers = [0, 1, 2, 3]
names = ['Thomas', 'Letice']

cnt = 0
result = product(letters, repeat=5)
for x in result:
    print(x)
    cnt += 1

# TODO: How to get the size in one line?

print(cnt)
