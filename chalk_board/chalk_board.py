from functools import wraps


class File:
    def __init__(self, filename, method):
        self.file = open(filename, method)

    # Needs to return the value to be used in the context manager
    # It will be assigned to the variable after keywork "as"
    def __enter__(self):
        print("__enter__")
        return self.file

    def __exit__(self, type, value, traceback):
        print("__exit__")
        self.file.close()
        # if we determine that the exception is fine, we return True
        if type == Exception:
            print("Handling exception")
            return True


with File("file.txt", "w") as f:
    print("~~writing~~")
    f.write("hello")
    # Notice how the __exit__ method gets called before the trace
    # Upon exception the context manager immediately goes to the
    # __exit__ function.
    raise Exception
    f.write("world")
    print("~~done~~")


class File:
    def __init__(self, filename, type):
        print("INIT")
        self.filename = filename
        self.type = type
        self.f = open(self.filename, self.type)

    def __enter__(self):
        print("ENTER")
        return self.f

    def __exit__(self, type, value, traceback):
        print("EXIT")
        f.close()
        if type:
            print(f"ERROR: ({type}, {value}, {traceback})")
            return True


with File("file.txt", "w") as f:
    print("writing")
    f.write("testing")
    x = 10 / 0


class File:
    def __init__(self, filename, operation, id):
        self.id = id
        print(f"{self.id}. Init")
        self.f = open(filename, operation)

    def __enter__(self):
        print(f"{self.id}. Entering")
        return self.f

    def __exit__(self, type, value, exception):
        print(f"{self.id}. Closing")
        self.f.close()
        if type:
            print(f"3. Error handled, error: ({type}, {value}, {exception})")
            return True


def logging(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with File("logger.txt", "a+", 4) as log:
            log.write(
                f"Function {f.__name__}: writing {next(a for a in args)}\n")
            print("4. writing")
            ret = f(*args, **kwargs)
            log.write(f"Function {f.__name__}: finished writing\n")
            return ret
    return wrapper


@logging
def write_file(what):
    with File("filename.txt", "w", 3) as f:
        print("3. writing")
        f.write(what)


write_file("hello world")
