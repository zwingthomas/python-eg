"""
Allows for undo/redo and the keeping of a chain of events. This is how
Ctrl+Z works. Essentially you keep a chain of events and with it a 
chain of states. This allows for you to store previous states without
the implementation details. Ctrl+Z has no idea what you actually did, 
it just knows how to get back ot the state you were in.

Briefly,
- Save and restore previous state without revealing implementation
    details
- 3 components:
    1. Memento - stores the state
    2. Originator - creates the state
    3. Caretaker - decides to save or restore the state
- Originally you have undo, one step backwards, and redo, one step 
    forward. However there is no real reason to limit to just that.

We are going to be making a simple implementation of storing state
that is overwritten one string at a time.

"""

from dataclasses import dataclass


@dataclass
class Memento:
    state: str


class Originator:
    def __init__(self, state):
        self.state = state

    def create_memento(self):
        return Memento(self.state)

    def restore_memento(self, memento: Memento):
        self.state = memento.state


class Caretaker:
    memento_list = []

    def save_state(self, state: Memento):
        self.memento_list.append(state)

    def restore(self, index: int):
        return self.memento_list[index]


if __name__ == "__main__":
    originator = Originator("initial state")
    caretaker = Caretaker()

    caretaker.save_state(originator.create_memento())
    print(f"Current state is {originator.state}")

    originator.state = "state 1"
    caretaker.save_state(originator.create_memento())
    print(f"Current state is {originator.state}")

    originator.state = "state 2"
    caretaker.save_state(originator.create_memento())
    print(f"Current state is {originator.state}")

    originator.restore_memento(caretaker.restore(1))
    print(f"Current state is {originator.state}")

    originator.restore_memento(caretaker.restore(0))
    print(f"Current state is {originator.state}")

    # An editor would go back one and forward one, but we can jump
    # around
    originator.restore_memento(caretaker.restore(2))
    print(f"Current state is {originator.state}")
