from collections import UserDict


class Box(UserDict):
    def __getattr__(self, key):
        # Allow attribute access for dictionary keys
        if key in self.data:
            return self.data[key]
        else:
            raise AttributeError(f"'Box' object has no attribute '{key}'")

    def __setatter__(self, key, value):
        # Allow setting attributes for dictionary keys
        if key == 'data':
            super().__setattr__(key, value)
        else:
            self.data[key] = value

    def __delattr__(self, key):
        # Allow deleting attributes
        if key in self.data:
            del self.data[key]
        else:
            raise AttributeError(f"'Box' object has no attribute '{key}'")


myself = Box({'name': 'Thomas', 'species': 'human', 'rank': 'the best'})

print(myself.name)
print(myself.species)
print(myself.rank)

myself.rank = "the worst"

print(myself.rank)

print(myself)
del myself.rank
print(myself)
