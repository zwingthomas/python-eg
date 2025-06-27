"""
The problem this is trying to solve is when you need to create a copy
of an object. The issue with just creating a new one is that the 
object you want to copy may have gone through some state changes or 
there is other complexity with the object. The issue with simple copying
is that there are private/not visible fields. We also may only have
the interface of the object and not know exactly what we are dealing
with. Generic copying would also mean that we are tightly coupled to 
the object.

Prototypes allow:
- Lets you copy existing objects
- Without depending on their classes
- Only reliant on their classes
- The copied object must provide the copy functionality
- Useful in testing and pre-production
"""
