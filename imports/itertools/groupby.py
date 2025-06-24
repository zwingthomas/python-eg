from itertools import groupby


def get_state(person):
    return person["state"]


people = [
    {"name": "Ava Hernandez",     "city": "Seattle",      "state": "Washington"},
    {"name": "Liam Patel",        "city": "Austin",       "state": "Texas"},
    {"name": "Sophia Thompson",   "city": "Denver",       "state": "Colorado"},
    {"name": "Noah Kim",          "city": "Atlanta",      "state": "Texas"},
    {"name": "Isabella Chen",     "city": "Boston",       "state": "Texas"},
    {"name": "Mason Rodríguez",   "city": "Phoenix",      "state": "Arizona"},
    {"name": "Mia Johnson",       "city": "Chicago",      "state": "Illinois"},
    {"name": "Ethan Williams",    "city": "Miami",        "state": "Florida"},
    {"name": "Olivia Martinez",   "city": "Portland",     "state": "Oregon"},
    {"name": "Lucas Anderson",    "city": "San Diego",    "state": "Oregon"},
    {"name": "Thomas Zwinger",    "city": "LA",           "state": "Texas"},
]


# WARNING groupby expects the people to be sorted by their group!

person_group = groupby(people, get_state)

for state, group in person_group:
    print(state)
    for person in group:
        print(person["name"], end=', ')
    print('\n')
