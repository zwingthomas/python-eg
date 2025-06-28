"""
In the most basic description, let's imagine we have two components
one is kind of a time intensive processing unit and on the other side
we have a user of this component which is waiting for it to finish. 
The naive implementation would have this polling the time intensive 
process until it eventually gets the return result "ready". However,
this scales incredibly poorly and could result in the time intensive
processing unit to be overloaded with polling. Instead we can implement
a registry in front of the time intensive process and the users 
register their interest in this result and they are the users are 
notified by the registry when their result is available. They can
also be only notified for type of results they are interested in.

Briefly,
- Defines a subscription mechanism
- Notify multiple objects simultaneously
    - Can also have multiple types of events notifying multiple
        interested parties
    - One to many, many to many, relationship

An example is an event generator which has an event manager that
talks with a SubscriberInterface that manages subscriptions to the
events.

"""

from abc import ABC, abstractmethod


class EventListener(ABC):
    @abstractmethod
    def update(self, event_type: str, file):
        ...


class EventManager:
    def __init__(self, operations):
        self.operations = operations
        self.listeners = {}
        # For each operation we have a list of listeners
        for op in operations:
            self.listeners[op] = []

    def subscribe(self, event_type: str, listener: EventListener):
        users = self.listeners[event_type]
        users.append(listener)

    def unsubscribe(self, event_type: str, listener: EventListener):
        users = self.listeners[event_type]
        users.remove(listener)

    def notify(self, event_type, file):
        users = self.listeners[event_type]
        [u.update(event_type, file) for u in users]


class Editor:
    events = EventManager(["open", "save"])
    file = None

    def open_file(self, file):
        self.file = file
        print(f"Editor: opening file {file}")
        self.events.notify("open", file)

    def save_file(self):
        print(f"Editor: saving file {self.file}")
        self.events.notify("save", self.file)


class EmailNotificationListener(EventListener):
    def __init__(self, email):
        self.email = email

    def update(self, event_type: str, file):
        print(
            f"Email to {self.email}: Someone has performed {event_type} operation on the file {file}")


class LogOpenListner(EventListener):
    def __init__(self, log_file):
        self.log_file = log_file

    def update(self, event_type: str, file):
        print(
            f"Save to log {self.log_file}: Someone has performed {event_type} operation on the file {file}"
        )


if __name__ == "__main__":
    editor = Editor()

    email_listener = EmailNotificationListener("test@gmail.com")
    log_listener = LogOpenListner("path/to/log/file.txt")

    editor.events.subscribe("open", log_listener)
    editor.events.subscribe("save", log_listener)

    editor.events.subscribe("save", email_listener)

    editor.open_file("test.txt")
    editor.save_file()
