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
print(function.__name__)
