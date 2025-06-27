"""
Very useful for when we have multiple inheritance in our code.
You can imagine a class that needs to inherit from multiple classes,
it will be composed of a certain number of other components. The
issue here is that the more of these components we have in our class
the more this class needs to handle different functionality in
different cases.

Think of the following:
A class that inherits Share and Color. It will need to handle the
combinations of Red, Blue, Yellow with Circle and Square. The more
these grow then this really gets out of hand. So it is better to have
Shape CONTAIN Color in a composition kind of way.

Having classes with mutliple orthogonal traits exponentially increases
the size of the inheritance tree.
- Convert from inheritance to composition.
- Split into multiple interfaces/classes
- Associate them using a "bridge reference"


"""

from abc import ABC, abstractmethod


class Device(ABC):
    volume = 0

    @abstractmethod
    def get_name(self) -> str:
        ...


class Radio(Device):
    def get_name(self) -> str:
        return f"Radio {self}"


class TV(Device):
    def get_name(self) -> str:
        return f"TV {self}"


class Remote(ABC):
    def volume_up(self):
        ...

    def volume_down(self):
        ...


class BasicRemote(Remote):
    def __init__(self, device: Device):
        self.device = device

    def volume_up(self):
        self.device.volume += 1
        print(f"{self.device.get_name()} volume up: {self.device.volume}")

    def volume_down(self):
        self.device.volume -= 1
        print(f"{self.device.get_name()} volume down: {self.device.volume}")


if __name__ == "__main__":

    """
    Even though we have two traits, the we use composition where the tv
    and radio HAVE a remote, instead of there being a remote associated
    with each one. Thus we can use the same remote class to control
    both the tv class and the radio class.

    TODO: Another example
    """
    radio = Radio()
    tv = TV()

    radio_remote = BasicRemote(radio)
    tv_remote = BasicRemote(tv)

    radio_remote.volume_up()
    radio_remote.volume_down()

    tv_remote.volume_up()
    tv_remote.volume_up()
    tv_remote.volume_up()
    tv_remote.volume_down()
