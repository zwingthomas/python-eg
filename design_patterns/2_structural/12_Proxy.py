"""
The proxy design pattern will allow us to have an interface or object
in front of an existing object in our code. The point is to manage
the lifecycle and control access to the object.

e.g.
We have a disk that takes quite a bit of time to write to and read from.
Then we have quite a few clients trying to write to and read from this
disk. All the clients may result in system overload and all of them
trying to access at the same time may corrupt the system. 
- One solution is to put a DiskProxy in front of the disk and provide
a cached version of the file. We could also put locks around files and
ensure that files are consistent. 

In brief:
- Provides some functionality before and/or after calling an object
- Same interface as the original object
    - e.g. Clients do not realize they are not accessing the real disk
- Similar to facade, except the proxy has the same interface
- Similar to decorator, except the proxy manages the lifecycle of the 
    object that it is hiding. Whereas the decorator simply replaces
    some functionality or adds its own before or after.

"""

from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def display(self):
        ...


class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        print(f"Real Image: loading {self.filename}")

    def display(self):
        print(f"Real Image: displaying {self.filename}", end="\n\n")


class ProxyImage(Image):
    """This is a proxy that applies a cache over loading an image"""

    def __init__(self, filename: str):
        self.filename = filename
        self.real_image = None

    def display(self):
        print(f"Proxy Image: displaying {self.filename}")
        if not self.real_image:
            print("from disk")
            self.real_image = RealImage(self.filename)
        else:
            print("from cache")
        self.real_image.display()


if __name__ == "__main__":
    image = ProxyImage("test.jpg")
    image.display()  # loads image from disk
    image.display()  # loads image from cache
