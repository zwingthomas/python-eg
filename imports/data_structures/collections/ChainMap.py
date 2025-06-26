from collections import ChainMap

d1 = {'orange': 1, 'apple': 2, 'watermelon': 2, 'grape': 4}
d2 = {'orage': 3, 'apple': 4, 'lemon': 2}

cm = ChainMap(d1, d2)  # Can chain many

print(cm)
print(cm["apple"])
print("Setting apple to 5 in ChainMap")
cm["apple"] = 5
print(d1)
print(d2)
print(cm)
print(f"Notice how lemon will default to d2 though: {cm['lemon']}")
print("Setting lemon to 6")
cm["lemon"] = 6
print(f"Now lemon is {cm['lemon']}")


# Especially helpful for setting environment variables
# ChainMap(cmd line arguments, env variables, static file config)
# This way if accesses to this ChainMap follow order of precedence
