from functools import wraps, update_wrapper
import time


def print_time(f):
    """This is a docstring for print_time"""
    # @wraps(f) # toggle this as a comment and run code
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        print(
            f"Function {f.__name__} took {time.perf_counter() - start: .2f} seconds to execute.")
        return result
    # update_wrapper(wrapper, f)  # toggle this and run code
    return wrapper


@print_time
def function():
    """This is a docstring for function"""
    time.sleep(1)
    print("End.")


function()
# Without @wraps(function) this returns the name of the wrapper, not the
# function
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
