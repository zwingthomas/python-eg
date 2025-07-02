# See Singleton.py in Design Patterns

# Nearly all practical metaclasses inherit from type, because that's
# the straightforward way to hook into a class construction and keep the
# full power of type's machinery

"""
But they don't **have** to. Any callable returning a class works. But
subclassing type is the most idiomatic and flexible approach. Take this
function for example see def simple_meta().

Key points:
- "Class of a class." A class object is an instance of its metaclass
- type is the default metaclass.
- It's not limited to dunders. Dunders are the hooks; the metaclass can
    execute arbitrary logic inside those hooks
- Use sparingly. Many tasks can be handled by decorators, descriptors,
    or class decorators. These are simpler, more pythonic, less
    surprising. Reach for a metaclass when you must influence class
    creation in a deep, reusable way.
"""


def simple_meta(name, bases, ns, **kw):
    cls = type(name, bases, ns)     # delegate to `type`
    cls.tag = "stamped by function"
    return cls


class Foo(metaclass=simple_meta):
    pass


Foo.tag                 # 'stamped by function'
isinstance(Foo, type)   # True – Foo *is* a class
# The metaclass used a *function*, but the
# resulting class is still an instance of `type`
type(Foo) is type


"""
A metaclass's job is to intercept and customize the moment a class
object is built and (optionally) how its instances are later created.
Overriding one or more "dunder" methods is how it hooks into those
two phases, but the effects you can achieve fo far beyond just
simply inheritance.

ORMs - Inspect class attributes, build a schema, register the model
Singleton/Pool - Override __call__ to cache or reuse instances
Pydantic - Collect Field() declaractions during class build
Automatic method decoration - Find every async def and wrap with retry
Plugin Registries - Each subclass auto-adds itself to registry[name] = cls

"""


class Registry(type):
    registry = {}

    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        Registry.registry[name] = cls           # auto-register
        return cls

    def __call__(cls, *args, **kw):
        print("Intercepting instance creation")
        return super().__call__(*args, **kw)    # then delegate


class Plugin(metaclass=Registry):
    pass


class Foo(Plugin):
    ...


class Bar(Plugin):
    ...


print(Registry.registry)   # {'Foo': <class '__main__.Foo'>, 'Bar': ...}
Foo()                      # prints the intercept message


"""
# Metaclass cheat-sheet
# ---------------------
# • **Class-creation phase** (runs once, when the class statement is executed)
#   • Hooks:
#       • __prepare__(mcls, name, bases, **kw)   # rarely needed
#       • __new__(mcls, name, bases, namespace, **kw)
#       • __init__(cls, name, bases, namespace, **kw)
#   • Possible uses:
#       • Modify / validate the class namespace before the class exists
#       • Auto-add mixins, properties, __slots__, docstrings, __repr__,
#           registries, SQL metadata
#       • Enforce rules (e.g. “every subclass must define Meta.pk”)
#
# • **Instance-creation phase** (runs every time you call the class)
#   • Hook:
#       • __call__(cls, *args, **kw)
#   • Possible uses:
#       • Enforce Singleton / Flyweight
#       • Return different subclasses (factory pattern)
#       • Inject dependency-injected parameters or other runtime behaviour
"""
