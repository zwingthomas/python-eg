from functools import WRAPPER_ASSIGNMENTS
from functools import wraps, update_wrapper
import time

# TODO: Review updated and assigned

"""
functools.update_wrapper() is the low-level helper that actually copies
dunder methods from the "real" function onto the wrapper after the 
wrapper object already exists.

functools.wraps() is a **decorator-factory** that **calls** 
update_wrapper() for you and returns a decorator. Use it in almost
every hand-written decorator. It is shorter, clearer, more pythonic,
and harder to forget.


They both:
- Copy a default set of attributes from wrapped to wrapper
- e.g. __module__, __name__, __qualname__, __doc__, __annotations__
- Merge the wrapped function's __dict__ into the wrappers
    - This way custom atttributes are not lost

They differ in only how you invoke them

When to prefer @wraps:
- Typical decorator function: the wrapper exists inside the decorator
- Readability / team style guide: one line instead of two, clear intent
- Harder to forget: If you omit these you get no error, more visible

When to prefer update_wrapper():
- Wrapper function elsewhere: it is not inside the decorator so you
    can't stick @wraps onto it
- Post-hoc patching: Sometimes you want to wrap later
    - attaching instrumentation around an object returned by another
        API
    - You create the wrapper first, then call 
        update_wrapper(wrapper, target) before you hand it back


"""


def print_time(f):
    """This is a docstring for print_time"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        print(
            f"Function {f.__name__} took {time.perf_counter() - start: .2f} seconds to execute.")
        return result
    return wrapper


@print_time
def function():
    """This is a docstring for function"""
    time.sleep(1)
    print("End.")


function()
# Without @wraps(function) or update_wrapper(wrapper, function)
# this returns the name of the wrapper, not the function
print(function.__name__)


print("-" * 12)
# Let's see what update_wrapper can do for us in this case


def print_time(f):
    """This is a docstring for print_time"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        print(
            f"Function {f.__name__} took {time.perf_counter() - start: .2f} seconds to execute.")
        return result
    update_wrapper(wrapper, f)  # <<<<<<<<<<<<<<<<<<<<<<<<<
    return wrapper


@print_time
def function():
    """This is a docstring for function"""
    time.sleep(1)
    print("End.")


function()
# Now this outputs the actual, correct metadata
print(function.__name__)


print("-" * 12)
# Let's see what @wraps(f) can do for us in this case
# This is the more pythonic approach


def print_time(f):
    """This is a docstring for print_time"""
    @wraps(f)  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        print(
            f"Function {f.__name__} took {time.perf_counter() - start: .2f} seconds to execute.")
        return result
    return wrapper


@print_time
def function():
    """This is a docstring for function"""
    time.sleep(1)
    print("End.")


function()
# Now the metadata is preserved in a pythonic way
print(function.__name__)

print("~~~~" * 12)
print("An example of update_wraps(), when you'd need to update later")
print("~~~~" * 12)
""" Custom dunder attributes """

# --------------------------------------------
# Our "real" function that carries some state
# --------------------------------------------


def real():
    pass


real.meta = {"author": "Alice"}            # a mutable dict attribute
# annotations are also a dict
real.__annotations__ = {"return": None, "test": "real"}

# Helper to print the two attributes we care about


def show(label, fn):
    print(f"{label:>9}: meta={fn.meta!r}, annotations={fn.__annotations__!r}")


show("real()", real)        # original state
print("-" * 52)


# ------------------------------------------------------------------
# 1) Wrapper WITHOUT 'updated'  → attributes are completely replaced
# ------------------------------------------------------------------
def make_plain_wrapper(target):
    def wrapper(*args, **kw):
        return target(*args, **kw)

    # store something *inside* the wrapper BEFORE we copy metadata
    wrapper.meta = {"created_by": "plain-wrapper"}
    wrapper.__annotations__ = {"note": "plain-wrapper"}

    # copy metadata – but NO merging for mutable attributes
    update_wrapper(wrapper, target,
                   assigned=("__name__", "__doc__"),
                   updated=())                     # <-- nothing gets merged
    return wrapper


plain = make_plain_wrapper(real)
show("plain()", plain)      # 'author' gone, annotations replaced
print("-" * 52)


# ------------------------------------------------------------------
# 2) Wrapper WITH 'updated'  → attributes are merged instead of clobbered
# ------------------------------------------------------------------
def make_merged_wrapper(target):
    def wrapper(*args, **kw):
        return target(*args, **kw)

    # store something first, just like before
    wrapper.meta = {"created_by": "merged-wrapper"}
    wrapper.__annotations__ = {"note": "merged-wrapper", "test": "merged"}

    # copy & MERGE dictionaries
    update_wrapper(wrapper, target,
                   assigned=("__name__", "__doc__"),
                   updated=("__dict__", "__annotations__"))  # <── merge these
    return wrapper


merged = make_merged_wrapper(real)
show("merged()", merged)
