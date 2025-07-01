import time


def timed(function):
    def wrapper(*args, **kwargs):
        before = time.perf_counter()
        value = function(*args, *kwargs)
        after = time.perf_counter()
        print(f"{function.__name__} took {round(after - before, 2)} second{'s' if after - before != 1 else ''} to execute")
        return value
    return wrapper


@timed
def myfunction(x):
    result = 1
    for i in range(1, x):
        if result == 0:
            result = 1
        result *= i
        result %= 1000
    return result


print(myfunction(100000000))
