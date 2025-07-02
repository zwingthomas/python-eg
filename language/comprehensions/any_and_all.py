names = ["Olivia", "Emma", "Sophia", "Isabella", "Mia", "Limma"]

print(any("mm" in name for name in names))  # output: True
print(any(len(name) < 3 in name for name in names))  # output: False
print(all(name.endswith("a") for name in names))  # output: True
print(all("i" in name for name in names))  # output: False

# Witness test
# witness is assigned to emma because Emma was the name that caused it
# it to shortcircuit and terminate the any statement. Thus, it was the
# last evaluated.
# TODO: Good use of walrus operator
print(any("mm" in (witness := name) for name in names))
print(witness)

# Counter example
# counter_example is assigned to Emma because that was the name that
# caused the any() call to short circuit so it was the last
# evaluated
print(all("i" in (counter_example := name) for name in names))
print(counter_example)
