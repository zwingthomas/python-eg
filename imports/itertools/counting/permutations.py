from itertools import permutations

# All the ways to group items where order does matter
letters = ['a', 'b', 'c', 'd', 'e']
numbers = [0, 1, 2, 3]
names = ['Thomas', 'Letice']

cnt = 0
result = permutations(letters, 2)
for x in result:
    print(x)
    cnt += 1

print(cnt)
