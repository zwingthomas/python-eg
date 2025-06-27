"""
This is one of the most useful design patterns. It allows us to hide 
away some complexity behind a simple interface. You might have a very
complex library and you do not want the client to have to understand
all the complexity that comes with the library. Instead, they should 
be able to just understand the simple facade that provides a front
to it. A facade does this by:

- Providing a simple interface to a complex functionality
- Removing the need for complex object / memory management
- Simplifies client implementation
- Abstraction

"""
from dataclasses import dataclass


class ComplexSystemStore:
    """We want to shield the user from this implemenation and complexity"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.cache = {}
        print(f"Reading data from file: {self.filepath}")

    def store(self, key: str, value: str):
        self.cache[key] = value

    def read(self, key: str):
        return self.cache[key]

    def commit(self):
        print(f"Storing cached data to file {self.filepath}")


@dataclass
class User:
    login: str


class UserRepository:
    """This is the facade that simplifies the above"""

    def __init__(self):
        self.system_preferences = ComplexSystemStore("/data/default.prefs")

    def save(self, user: User):
        self.system_preferences.store("USER_KEY", user.login)
        self.system_preferences.commit()

    def find_first(self):
        return User(self.system_preferences.read("USER_KEY"))


if __name__ == "__main__":
    # Notice we only interact with the facade
    user_repo = UserRepository()
    user = User("Thomas")
    user_repo.save(user)
    retrieved_user = user_repo.find_first()
    print(retrieved_user.login)
