# Acknowledgements____

# Corey Schafer
# Python Tutorial: Iterators and Iterables - What Are They and How Do They Work?
# https://www.youtube.com/watch?v=jTYiNjvnHZY&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=3&ab_channel=CoreySchafer

# Python and Pandas with Reuven Lerner
# Python interview question #33: Iterator protocol
# https://www.youtube.com/watch?v=SwZTybphARU&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=4&ab_channel=PythonandPandaswithReuvenLerner

# What is the iteration protocol in Python?
# 1. is the object iterable?
# 2. if you are iterable, then give me your next item
# 3. repeat (2) until we get a StopIteration exception

# A list is an iterable, it is not an iterator
# When something is iterable all it means at a high level is that it can
# be looped over.

nums = [1, 2, 3]

for num in nums:
    print(num)

# Also works for tuples, dictionaries, strings, files, all sorts of
# objects... why is this? How do we tell if something is iterable?


# All iterators will have a special method __iter__()

print("__iter__" in dir(nums))  # outputs: True

# Iterators get their next value with the __next__ method, lists do not
# have __next__. They do not know where they are or their state.

try:
    print(next(nums))
except TypeError as e:
    print(e)

# Let's create an iterator from our nums iterable.
i_nums = nums.__iter__()
print("__next__" in dir(i_nums))  # outputs: True

# This iterator is what is passed to the for loops. If it did not
# pass in a fresh __iter__ everytime, then it would be exhausted upon
# looping over it once like a stack. For loops know how to handle
# these StopIteration exceptions for us, while loops do not. You can
# build for loops with while loops, thus only a while loop is requisite
# for a language

try:
    while True:
        print(next(i_nums))
except StopIteration as stop:
    print("Stopping.")


# Lets create a class that behaves like the default range function

class MyRange:

    def __init__(self, start, end):
        self.value = start
        self.end = end

    # For something to be iterable, it needs this method
    def __iter__(self):
        return self

    # Since we're returning self we need this object to have __next__
    def __next__(self):
        if self.value >= self.end:
            raise StopIteration
        current = self.value
        self.value += 1
        return current


nums = MyRange(1, 10)

print("Print once")
for num in nums:
    print(num)

print("Print again")
for num in nums:
    print(num)
print("Notice how it is now exhausted so nothing printed out because it did not pass an actual __iter__ that implemented __next__. Instead it returned self from __iter__ which then called __next__ on itself. Exhausting the iterator.")
# TODO: Implement a way that avoids it being exhausted, do it on your own

# The same behavior can be created with generators


def my_range(start, end):
    current = start
    while current < end:
        yield current
        current += 1


print("\nImplementing the same functionality with generators")
generator = my_range(1, 10)

for num in generator:
    print(num)

print("Notice is also gets exhausted by looping through once")
for num in generator:
    print(num)

# TODO: Make a custom generator with iter.
