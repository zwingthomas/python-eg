# Acknowledgements____
# Corey Schafer
# Python Tutorial: Sets - Set Methods and Operations to Solve Common Problems
# https://www.youtube.com/watch?v=r3R3h5ly_8g&ab_channel=CoreySchafer

"""
Sets are very performant with membership tests, they also allow for
some pretty cool operations between them and other collections.
"""

# Create an empty set
hash_set = set()
print(hash_set)

# Create a set with numbers
hash_set = {1, 2, 2, 2, 3, 3, 3, 3, 4, 5}
print(hash_set)

# .add method
hash_set.add(7)
print(hash_set)

# Add new numbers with .update
hash_set.update([17, 18, 19, 20])
print(hash_set)

# Add sets together using .update
hash_set2 = {12, 13, 4, 3, 2, 2}
hash_set.update(hash_set2)
print(hash_set)

# Remove number within the set
hash_set.remove(2)

# Remove number no longer in set
try:
    hash_set.remove(2)
except KeyError as e:
    print("Key Error: ", e)

hash_set.add(2)

# Discard number within the set
hash_set.discard(2)

# Discard number no longer in set, notice this does not throw any
# exception
hash_set.discard(2)

#
# Set Operations
#

s1 = {1, 2, 3}
s2 = {2, 3, 4}
s3 = {3, 4, 5}
print("s1", s1)
print("s2", s2)
print("s3", s3)
print("all_in_common:",
      s1 & s2 & s3,
      s1 & s2 & s3 == s1.intersection(s2, s3))
print("values_in_s1_not_in_s2:",
      s1 - s2,
      s1.difference(s2) == s1 - s2)
print("values_in_s2_not_in_s1_or_s3:",
      s2 - (s1 | s3),
      s2 - (s1 | s3) == s2.difference(s1, s3))
print("values_unique_to_both_s1_and_s2",
      (s1 - s2) | (s2 - s1),
      (s1 - s2) | (s2 - s1) == s1.symmetric_difference(s2))
hash_set = set()
# This does not return anything, it is in place
hash_set.update(s1, s2, s3)
print("values_in_all_sets",
      s1 | s2 | s3,
      s1 | s2 | s3 == hash_set)

#
# NOTE: All of the x.set_method(y, z) can be done with y and z as either
#        a set or with y and z as lists.
#
