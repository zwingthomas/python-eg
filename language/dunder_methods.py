# Acknowledgements____
# Tech with Tim
# Please Master This MAGIC Python Feature... 🪄
# https://www.youtube.com/watch?v=qqp6QN20CpE&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=5&ab_channel=TechWithTim


# Dunder/Magic methods

"""
Classes have these dunder/magic methods that allow you to map
behavior from a class. There is __init__ that defines behavior of the
class when the class is created. There is __add__ that defines the
addition operator. There are many others. Remember, everything you
create in Python is an object. These essentially allow you to use the 
Python syntax features with your object.
"""


from dataclasses import dataclass


def func():
    pass


print(type(func))  # Notice how this is an Object of the class function

str1 = "Hello"
str2 = "World"
print(str1 + str2)
print(str1.__add__(str2))  # Notice how these are the same
print(len(str1))
print(str1.__len__())  # Notice how these are the same

"""
Dunder methods essentially map to the operators we use in our code.
You can make them custom!
"""


class Counter:
    def __init__(self):
        self.value = 1

    def count_up(self):
        self.value += 1

    def count_down(self):
        self.value -= 1

    def __add__(self, other):
        if isinstance(other, Counter):
            return self.value + other.value
        else:
            raise TypeError("Invalid Type")


count1 = Counter()
count2 = Counter()

count1.count_up()
count2.count_up()

print(count1, count2)
print(count1 + count2)

"""
Always implement str and repr on custom objects to make debugging 
easier.
"""


@dataclass
class Car:
    make: str
    model: str
    year: int

    # Basic output
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    # Developer friendly output
    def __repr__(self):
        return f"Car({self.year=} {self.make=} {self.model=})"


my_car = Car('Chevy', 'Impala', 2007)
print(str(my_car))
print(repr(my_car))


"""
Lets get into some more to understand better how in-depth these go.
"""


class InventoryItem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"InventoryItem({self.name=}, {self.quantity=})"

    def __add__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem(self.name, self.quantity + other.quantity)
        raise TypeError("Cannot add items of different types.")

    def __sub__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            if self.quantity > other.quantity:
                return InventoryItem(self.name, self.quantity + other.quantity)
            raise ValueError("Cannot subtract more than available quantity.")
        raise TypeError("Cannot subtract items of different types.")

    def __mul__(self, factor):
        if isinstance(factor, (int, float)):
            return InventoryItem(self.name, int(self.quantity * factor))
        raise TypeError("Multiplication factor must be a number.")

    def __truediv__(self, factor):
        if isinstance(factor, (int, float)) and factor != 0:
            return InventoryItem(self.name, int(self.quantity / factor))
        if factor == 0:
            raise ValueError("Division factor must be a nonzero number.")
        raise TypeError("Division factor must be a nonzero number.")

    def __floordiv__(self, factor):
        if isinstance(factor, (int, float)) and factor != 0:
            return InventoryItem(self.name, int(self.quantity // factor))
        if factor == 0:
            raise ValueError("Division factor must be a nonzero number.")
        raise TypeError("Division factor must be a nonzero number.")

    def __eq__(self, other):
        if isinstance(other, InventoryItem):
            return self.name == other.name and self.quantity == other.quantity
        return False

    def __lt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity < other.quantity
        if self.name != other.name:
            raise ValueError("These are not the same item.")
        raise TypeError("Cannot compare items of different types.")

    def __gt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity > other.quantity
        if self.name != other.name:
            raise ValueError("These are not the same item.")
        raise TypeError("Cannot compare items of different types.")

    # TODO: __getstate__ & __setstate__


item1 = InventoryItem("Apple", 50)
item2 = InventoryItem("Apple", 30)
item3 = InventoryItem("Orange", 10)

print(repr(item1 + item2))
try:
    item1 + item3
except TypeError as e:
    print(e)


"""
Let's see how storing information and making it retrivable with 
dunder methods can be a performance boost to your objects
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        """Do not recalculate, just return the size directly"""
        return self.size

    def __getitem__(self, index):
        """Retrieve an item (obj[index])"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range.")
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def __setitem__(self, index, value):
        """Enable item assignment (obj[index] = value)"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range.")
        current = self.head
        for _ in range(index):
            current = current.next
        current.value = value

    def __delitem__(self, index):
        """Delete an item (del obj[index])"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range.")
        if index == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            current.next = current.next.next
        self.size -= 1

    def __contains__(self, value):
        """Define behavior of 'in' keyword"""
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def append(self, value):
        """Add a new node to the end of the list"""
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def __str__(self):
        """User friendly string representation"""
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " -> ".join(values)


l1 = LinkedList()
l1.append(10)
l1.append(20)
l1.append(30)
print(l1)
print(f"len(l1): {len(l1)}")
print(f"l1[1].value: {l1[1].value}")
l1[1] = 25
print(l1)
del l1[1]
print(l1)


"""
You can even use dunder/magic methods to implement ContextManagers!!!
"""


class DatabaseConnection():
    def __init__(self, name):
        self.name = name
        self.connected = False

    def __enter__(self):
        self.connected = True
        print(f"Connected to the database '{self.name}'.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connected = False
        print("Disconnected from the database '{self.name}'.")
        if exc_type:
            print(
                f"An exception occured: {exc_type=} {exc_value=} {traceback=}")
        return True


with DatabaseConnection("ExampleDB") as db:
    print(f"Is connected? {db.connected}")
    raise Exception


"""
Dunder/magic methods are also how Iterators work! Look into python-eg/language/iterators_and_iterables.py for more information on these
"""
