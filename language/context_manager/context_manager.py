# Acknowledgement____
# Tech with Tim
# Expert Python Tutorial #6 - Context Managers
# https://www.youtube.com/watch?v=Lv1treHIckI&ab_channel=TechWithTim

import contextlib
file = open("file.txt", "w")
file.write("hello")  # What happens if there is an exception here?
file.close()  # You will have opened the file and never closed it

# Could do
file = open("file.txt", "w")
try:
    file.write("hello")
finally:
    file.close()

# Better to do
with open("file.txt", "w") as file:
    file.write("hello")


"""
Context managers are a way to ensure you do one operation after
performing another operation. This is very important and useful for
shared memory, locks, and files.
"""


class File:
    def __init__(self, filename, method):
        self.file = open(filename, method)

    # Needs to return the value to be used in the context manager
    # It will be assigned to the variable after keywork "as"
    def __enter__(self):
        print("__enter__")
        return self.file

    def __exit__(self, type, value, traceback):
        print("__exit__")
        self.file.close()
        # if we determine that the exception is fine, we return True
        if type == Exception:
            print("Handling exception")
            return True


with File("file.txt", "w") as f:
    print("~~writing~~")
    f.write("hello")
    # Notice how the __exit__ method gets called before the trace
    # Upon exception the context manager immediately goes to the
    # __exit__ function.
    raise Exception
    f.write("world")
    print("~~done~~")


"""
With contextlib import we can decorate a generator that becomes a 
context manager. This is a quicker and easier way to make a context
manager.
"""


@contextlib.contextmanager
def file(filename, method):
    print("enter")
    file = open(filename, method)
    yield file
    file.close()
    print("exit")


with file("text.txt", "w") as f:
    print("~~writing in the generator context manager~~")
    f.write("hello from a generator context manager")
