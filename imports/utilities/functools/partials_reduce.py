from functools import partial, partialmethod, reduce
from urllib.request import urlopen


# Partials
def get_site_status(url: str, test: int) -> int:
    print(test)
    try:
        return urlopen(url).getcode()
    except:
        return "ERROR"


google_status = partial(get_site_status, "https://google.com", 0)
print(google_status())
facebook_status = partial(get_site_status, "https://facebook.com", 0)
print(facebook_status())
traxy_status = partial(get_site_status, "https://traxy.app", 0)
print(traxy_status())


# Partialmethods
class VMManager:
    def toggle_power(self, to_state, type):
        if to_state == "on":
            print(f"Powering on VM: {type}")
        if to_state == "off":
            print(f"Powering off VM: {type}")

    power_on_linux = partialmethod(toggle_power, "on", "Linux")
    power_off_linux = partialmethod(toggle_power, "off", "Linux")
    power_on_windows = partialmethod(toggle_power, "on", "Windows")
    power_off_windows = partialmethod(toggle_power, "off", "Windows")


admin = VMManager()
admin.power_on_linux()
admin.power_off_linux()
admin.power_on_windows()
admin.power_off_windows()


# Reduce
def multiply(a, b):
    print(f"{a=} multiplied by {b=}: {a * b}")
    return a * b


reduce(multiply, range(1, 5))

# Reduce and partial
factorial = partial(reduce, multiply)
factorial(range(1, 5))
