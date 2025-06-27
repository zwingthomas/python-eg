# The simpler way to construct a builder with Python

class NetworkService:
    def __init__(self, url: str = "", auth: str = "", cache: int = 0):
        self.components = {}
        if url:
            self.components["URL"] = url
        if auth:
            self.components["Authorization"] = auth
        if cache:
            self.components["Cache-Control"] = cache

    def show(self):
        print(self.components)


if __name__ == "__main__":
    service1 = NetworkService(url="traxy.app")
    service1.show()

    service2 = NetworkService(url="youtube.com", auth="test123", cache=40000)
    service2.show()

# This is equivalent to what is shown in 4a_Builder and much easier to
# maintain. This is only possible in languages like Python where
# parameters themselves are optional.
