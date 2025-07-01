# Acknowledgements
# Indently
# How To Create Custom Exceptions In Python
# https://www.youtube.com/watch?v=CK0wc85inxk&ab_channel=Indently


from typing import Any
import pickle


class HardwareError(Exception):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f"{self.message} (Value: {self.value})"

    # This ensures that when you try to pickle your value, that all
    # the values are included and the type is preserved
    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


overheat_exception: HardwareError = HardwareError(
    message='Computer overheated', value=137)

print(overheat_exception)
print(repr(overheat_exception))
print(overheat_exception.message)
print(overheat_exception.value)

try:
    raise HardwareError('Laptop is too hot', 101)
except HardwareError as e:
    print(e)
    print(e.message)
    print(e.value)


OE: HardwareError = HardwareError('Laptop is too hot', 101)
print(repr(OE))

# In order to pickle this object you need to have the __reduce__
# dunder method defined!
pickled: bytes = pickle.dumps(OE)
unpickled: HardwareError = pickle.loads(pickled)

print(repr(unpickled))
print(unpickled.message)
print(unpickled.value)
