def logged(function):
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        # TODO what all can a+ be here instead, what does a+ mean?
        with open('logfile.txt', 'a+') as f:
            fname = function.__name__
            print(f"{fname} returned value: {value}")
            f.write(
                f"{fname} with {args if args else ''} {kwargs if kwargs else ''} returned value: {value}\n")
        return value
    return wrapper


@logged
def add(x, y):
    return x + y


print(add(10, 20))
