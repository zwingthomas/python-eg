"""
Most widely talked about and known about design pattern. There are 
many positives and negatives to this design pattern.

Let's say we had 3 components that need to communicate with the 
network. A naive way would be to instantiate a network component every
time you wanted to communicate with the network. This is inefficient
you would not want to create 3 instances that do the same thing. You
may instead just want one instance. This would allow you to order the
network calls by importance and also it is good for testing as you are
able to test just the single resource.

Briefly,
- Only one possible instance
- Single point of access for a resource
- Uses:
    - Network manager
    - Database access
    - Logging
    - Utility class(es)
- Disadvantages:
    - Breaks single responsibility: meaning that a singleton will 
        manage its own state and allow others to create only one 
        instance. A particular class should create a component when
        required whereas a singleton creates its own instance.
    - Testability issues: when you have only one instance you are 
        tightly coupled with the components that need that instance. 
        Thus you cannot really mock a singleton instance: fixtures
    - State for life: once a singleton has been instantiated you only
        have that one instance forever. You could kill it given 
        certain circumstances but that works against the singleton
        pattern.

#TODO: Mezmorize this implementation
"""

# Naive implementation that will not work in a multi-threaded
# environment.

from threading import Thread, Lock
import time


class Singleton(type):
    _instances = {}
    _lock = Lock()  # comment out to experiment

    def __call__(self, *args, **kwargs):
        with self._lock:  # comment out to experiment
            if self not in self._instances:
                instance = super().__call__(*args, **kwargs)
                time.sleep(1)
                self._instances[self] = instance
        return self._instances[self]


class NetworkDriver(metaclass=Singleton):
    # TODO: inspect
    """Think of Python objects as a two-tier system
        instance -> class -> *metaclass* 
        - Instances are created by their class dog = Dog()
        - A class is itself an object created by another class called 
            its "metaclass".
        - By default, every user-defined class is built by the built-in
            metaclass type.
        - A metaclass can intercept or customize the moment a class is
            constructed and/or called, because it inherits type and 
            overrides special methods such as __new__, __init__ or, as
            in this example, __call__
        - Singleton in this case **is** a metaclass as it inherits from
            type
        - __call__ will run on any class that lists Singleton as its
            metaclass
        """

    def log(self):
        print(f"{self}")


def create_singleton():
    singleton = NetworkDriver()
    singleton.log()
    return singleton


if __name__ == "__main__":
    # single thread
    # s1 = create_singleton()
    # s2 = create_singleton()
    # print(f"Are they the same? {s1 == s2}")

    # multithread
    p1 = Thread(target=create_singleton)
    p2 = Thread(target=create_singleton)
    p1.start()
    p2.start()

    # Need to add a lock!
    # Lock has been added. Now you see they are the same object.
