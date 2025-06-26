from itertools import combinations_with_replacement


# All the ways to group items where order does not matter and there can
# be repeats
letters = ['a', 'b', 'c', 'd', 'e']
numbers = [0, 1, 2, 3]
names = ['Thomas', 'Letice']

cnt = 0
result = combinations_with_replacement(letters, 10)
for x in result:
    print(x)
    cnt += 1

# TODO: How to get the size in one line?

print(cnt)
