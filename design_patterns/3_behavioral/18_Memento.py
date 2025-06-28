"""
Allows for undo/redo and the keeping of a chain of events. This is how
Ctrl+Z works. Essentially you keep a chain of events and with it a 
chain of states. This allows for you to store previous states without
the implementation details. Ctrl+Z has no idea what you actually did, 
it just knows how to get back ot the state you were in.

Briefly,
- 
"""
