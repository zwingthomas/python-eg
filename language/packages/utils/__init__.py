
# Notice when you run imports, this file runs. This is to set up
# some configs or other set up operations generally for larger imports.

from .string_util import capitalize
from .math_util import add

# Ensure you place the single dot in from so that you get the relative
# import and tell it to look in the current package

# With this however, it will not know how to run directly as it does
# not know it is inside the package. You need to change how the imports
# are managed based on the entrypoint. This can be done with
# if __name__ == "__main__"

print("imported utils")

COLOR = "Red"
# You can simplify the imports. Generally you'd have to import imports
# with
# from utils.string_util import capitalize
# from utils.math_util import add
# However if you add the imports with file has, you are now able to
# directly import from just utils. This is much cleaner and makes a
# lot more sense.
