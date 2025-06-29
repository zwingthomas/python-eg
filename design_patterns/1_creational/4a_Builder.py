"""
The Builder pattern is used when we have multiple parametes to 
initialize. For many parameters, it's impractical to build all 
constructors.

5 parameter combinations -> 120 constructor variants

Many of the times you have optional parameters, and it should also be
easy to read the object and how to use it.

There are two ways to do the builder pattern, one more simple and one
more classical.

"""

# The classic way to build a builder

class NetworkService:
    def __init__(self):
        self.components = {}

    def add(self, key: str, value: str):
        self.components[key] = value

    def show(self):
        print(self.components)


class NetworkServiceBuilder:
    def __init__(self):
        self._service = NetworkService()

    def add_target_url(self, url: str):
        self._service.add("URL", url)

    def add_auth(self, auth: str):
        self._service.add("Authorization", auth)

    def add_cache(self, cache: int):
        self._service.add("Cache-Control", cache)

    def build(self) -> NetworkService:
        service = self._service
        self._service = NetworkService()
        return service


if __name__ == "__main__":
    builder = NetworkServiceBuilder()
    builder.add_target_url("traxy.app")

    service1 = builder.build()
    service1.show()

    builder.add_target_url("youtube.com")
    builder.add_auth("test123")
    builder.add_cache(40000)

    service2 = builder.build()
    service2.show()
