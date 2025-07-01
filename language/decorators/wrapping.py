# Acknowledgements
# Decorators - Advanced Python Tutorial #2
# https://www.youtube.com/watch?v=iZZtEJjQLjQ&ab_channel=NeuralNine


# This is how wrappers look like without the @ symbol
# This does not preserve metadata

def mydecorator(function):
    def wrapper():
        print("I am decorating your function")
        function()
        print("Done with function")

    return wrapper


def hello_world():
    print("Hello world!")


mydecorator(hello_world)()

print("-" * 12)
# We use annotations to do this in a more pythonic way
# Right now it doesn't pass parameters and metadata is not preserved


def mydecorator(function):
    def wrapper():
        print("I am decorating your function")
        function()
        print("Done with function")

    return wrapper


@mydecorator
def hello_world():
    print("Hello world!")


hello_world()

print("-" * 12)
# Let's get it so that it can pass arguments, keep in mind this
# wrapper may be wrapping a bunch of different functions with a bunch
# of different arguments for each
# This still doesn't preserve metadata, also there's no return!


def mydecorator(function):
    def wrapper(*args, **kwargs):
        print("I am decorating your function")
        function(*args, **kwargs)
        print("Done with function")

    return wrapper


@mydecorator
def hello_world(name):
    print(f"Hello {name}!")


hello_world("Thomas")


print("-" * 12)
# Now we are returning from the function, but notice we can't do
# anything after the function :L


def mydecorator(function):
    def wrapper(*args, **kwargs):
        print("I am decorating your function")
        return function(*args, **kwargs)
        print("Done with function")

    return wrapper


@mydecorator
def hello_world(name):
    return f"Hello {name}!"


print(hello_world("Thomas"))

print("-" * 12)
# To accomplish this we must store the return and return after
# This still does not preserve metadata


def mydecorator(function):
    def wrapper(*args, **kwargs):
        print("I am decorating your function")
        ret = function(*args, **kwargs)
        print("Done with function")
        return ret

    return wrapper


@mydecorator
def hello_world(name):
    return f"Hello {name}!"


print(hello_world("Thomas"))
