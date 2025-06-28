"""
Conceptually this design pattern is about linking handlers to one
another, feeding the output of one into the input of anohter passing
it up the chain. Or it could consume the request at any point in the 
chain depending on the logic. This allows for very flexible pipelines
where different requests will be managed by the same sequence of 
handlers, just different amounts of handlers. Maybe the handlers will
skip the request entirely as well.

Briefly:
- Defines a chain of handlers to process a request
- Each handler contains a reference to the next handler
- Each handler decides to process the request AND / OR pass it on
- Requests can be of different types
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class HandlerChain(ABC):
    def __init__(self, input_header: HandlerChain):
        self.next_header = input_header

    @abstractmethod
    def add_header(self, input_header: str):
        ...

    def do_next(self, input_header: str):
        if self.next_header:
            return self.next_header.add_header(input_header)
        return input_header


class AuthenticationHeader(HandlerChain):
    def __init__(self, token: str, next_header: HandlerChain = None):
        super().__init__(next_header)
        self.token = token

    def add_header(self, input_header: str):
        h = f"{input_header}\nAuthorization: {self.token}"
        return self.do_next(h)


class ContentTypeHeader(HandlerChain):
    def __init__(self, content_type: str, next_header: HandlerChain = None):
        super().__init__(next_header)
        self.content_type = content_type

    def add_header(self, input_header):
        h = f"{input_header}\nContentType: {self.content_type}"
        return self.do_next(h)


class BodyPayloadHeader(HandlerChain):
    def __init__(self, body: str, next_header: HandlerChain = None):
        super().__init__(next_header)
        self.body = body

    def add_header(self, input_header: str):
        h = f"{input_header}\n{self.body}"
        return self.do_next(h)


if __name__ == "__main__":
    # Create the handlers
    authentication_header = AuthenticationHeader("test123")
    content_type_header = ContentTypeHeader("json")
    body_header = BodyPayloadHeader("Body: {'username': 'Thomas'}")

    # Link up the chain
    authentication_header.next_header = content_type_header
    content_type_header.next_header = body_header

    # Go through the entire chain
    message_with_authentication = authentication_header.add_header(
        "Header with authentication")
    # Start from a different place in the chain depending on request
    message_without_authentication = content_type_header.add_header(
        "Header without authentication")

    print()
    print(message_with_authentication)
    print()
    print(message_without_authentication)
    print()
