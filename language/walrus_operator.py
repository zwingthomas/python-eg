# Assignment expression operator (Python 3.8)

a = 42  # nothing is returned: assignment
a + 7  # something is returned: expression
try:
    # can output, something is returned to print
    print(f"Do an expression {a + 7}")
    print(f"a is unchanged: {a}")
    # can output, something is returned to print
    print(f"Assign and return " + str(a := 30))
    print(f"a is now {a}")  # outputs: 30
    print(
        f"Notice this doesn't work with fstrings without parenthesis \
            {(a := 32)}")
    print(a=42)  # cannot output, nothing is returned to print
except TypeError as e:
    print(e)


# Now the distance, d,  is only in the scope of the if-clause,
# not global
def distance(a, b):
    return abs(a - b)


if (d := distance(2, 5)) < 4:
    print(f"distance {d} is less than 4")


a = 0
b = 8
while (d := distance(a, b)) > 3:
    print(f"The distance between a and b is {d}")
    a += 1


names = ["Olivia", "Emma", "Sophia", "Isabella", "Mia"]
