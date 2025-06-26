from collections import Counter

s = "This is a sentence with some letters in it"
cnt = Counter(s)
print(cnt)
cnt_of_t = cnt['T'] + cnt['t']
print(cnt_of_t)

print(list(cnt.elements()))
print(cnt.most_common(3))
print(cnt.total())

# Generate a list with elements
print(list(Counter(x=10, y=4).elements()))
