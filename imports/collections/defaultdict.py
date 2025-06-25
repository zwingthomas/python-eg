from collections import defaultdict

word_list = ["orange", "apple", "watermelon",
             "apple", "watermelon", "grape", "apple"]

hm = defaultdict(int)
print(hm["apple"])  # No error with defaultdict
for word in word_list:
    hm[word] += 1
print(hm["apple"])


def infinite_dict():
    return defaultdict(infinite_dict)


infiniteDict = infinite_dict()
print(infiniteDict)
print('\n')
infiniteDict["one"]["two"]["three"]["four"] = 42
print('\n')
print(infiniteDict)
infiniteDict["one"]["two"]["another"] = 3
print('\n')
print(infiniteDict)
