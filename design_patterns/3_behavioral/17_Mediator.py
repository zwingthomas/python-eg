"""
The mediator pattern is very useful when you have a bunch of things
that need to process individually and communicate with eachother.
Think, a distributed system. The nodes need to be aware of one another
which is obviously a problem when the system grows. 

A mediator allows for a central location that forwards messages based
on who the reciever should be. This is sort of how DNS works. This is
also how chat applications work. 

Briefly,
- Provides a central object used for communicating between objects
- Objects don't talk to each other
- Reduce dependencies between objects

In our example we will make a group chat with several users that can
all communicate through one mediator.
"""

from __future__ import annotations


class ChatUser:
    mediator = None

    def __init__(self, name: str):
        self.name = name

    def set_mediator(self, med: Mediator):
        self.mediator = med

    def send(self, msg: str):
        print(f"{self.name}: Sending message {msg}")
        self.mediator.send_message(msg, self)

    def recieve(self, msg: str):
        print(f"{self.name}: Recieving message {msg}")


class Mediator:
    users = []

    def add_user(self, user: ChatUser):
        self.users.append(user)
        user.set_mediator(self)

    def send_message(self, msg: str, user: ChatUser):
        for u in self.users:
            if u != user:
                u.recieve(msg)


if __name__ == "__main__":
    mediator = Mediator()

    alice = ChatUser("Alice")
    bob = ChatUser("Bob")
    carol = ChatUser("Carol")

    mediator.add_user(alice)
    mediator.add_user(bob)
    mediator.add_user(carol)

    carol.send("Hi everyone!")
