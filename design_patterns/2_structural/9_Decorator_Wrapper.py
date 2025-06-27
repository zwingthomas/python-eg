"""
Called either the decorator or the wrapper patern. It is very useful
and easy to understand. It allows us to modify the behavior of a 
function, method or a class that we do not fully have control over.

- Attach new behavior to an object
- Without altering existing code
- Overriding behavior
- Centralize functions

E.g.
Imagine you have a TCP/IP protocol that has a sendPacket() functionality.
This send packet functionality will not suffice as we want to communicate
with an API that we do not control. We could put a wrapper on top of this
In order to communicate between them. You could even go further and wrap
directly to the API service you want it to communicate to.

"""
