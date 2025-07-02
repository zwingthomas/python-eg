# Acknowledgements____
# ByteByteGo
# How the Garbage Collector Works in Java, Python, and Go!
# https://www.youtube.com/watch?v=3Kqal7QaCCM&ab_channel=ByteByteGo

# NeuralNine
# Garbage Collection in Python: Speed Up Your Code
# https://www.youtube.com/watch?v=pVGujarYk9w&ab_channel=NeuralNine

"""
Basic overview of garbage collection in OOP languages__________
"""
"""

Garbage collection makes programming in modern language a lot easier.
They manage memory for you. Without them or effective memory management
you would be left with a program that consumes more and more memory.
With them, things no longer in use get disposed of: freeing up space
in the stack and heap.

# TODO: What is the difference between the stack and heap? You know this.

There is the concept of reachibility. All programs have GC Roots. These
are global variables and things that exist throughout the entire life
of the application. Then, anything that can be reached from these roots
is also considered alive and must be kept. Everything else is garbage, 
ready to be collected. 

Objects start life in the Young Generation's Eden Space. Then they 
go into the Survivor Space. The Survivor Space is further divided into
s0 and s1, however it is still in the Young Generation. Most objects
will die in the Eden Space. But if they survive multiple cycles they
are promoted through the Survivor Space layers and eventually
into the Old Generation: where garbage collection happens less 
frequently.

mark and sweep
The most fundamental garbage collection algorithm is the mark and 
sweep algorithm. It works in two phases:
1. During the mark phase it traverses all references from the GC Roots
2. During the sweep phase it cleans up everything not traversed
This is bad because it has to pause the entire application during 
clean up.

Try-caller mark and sweep
The try-caller mark and sweep algorithm reduces these pauses. This 
still traverses. But now it marks references in three groups: white,
grey, and black.
- White objects are considered potential garbage
- Grey objects are known to be reachable but have not been fully explored
- Black objects are known to be reachable and have been fully processed
With this the application pauses briefly for inital marking and then
continue examining grey objects while the applciation runs.

Python's garbage collection
Python uses a combination of reference counting and a cyclic reference
garbage collection. Most things are cleaned up by counting when the
references drop to zero. But some things with circular references
can't be cleaned up with just regular reference counting so it needs
its own management system.

Issues with garbage collection
- Pauses can happen unpredicably
- Memory can become fragmented, slowing down allocation over time
    - This is avoided by properly managing used pools and free pools
- Performance overhead
"""

"""
Theoretical on Python Specifically__________
"""
"""
As things reference eachother

like temp.name = c, b[x] = c

Things get references counted up and up. So c would have 2 references.
Once a and b are deleted then c can be freely garbage collected as its
reference count has dropped to zero.

There are issues like cyclic references though:
      
temp -> b1 <-> b2 <-> b3 <-> b1

Since all the b's are linked up cyclically, even if we were to delete
all of the b's. None of them would be garbage collected as a still 
points to b1 and all of the references are still in place! There is 
still a path from a to b1, b2, and b3. Thus you cannot really destroy
these objects, you can still reach them. However, if you just has

b4 <-> b4

When you delete b4 nothing is pointing to b4 anymore so it can be 
garbage collected.

# TODO: How does Python garbage collect cyclic references then?


In Python there are three generations: g0, g1, and g2. All objects
start in g0. After a certain threshold (700) of allocations the garbage 
collector fires up. There will be many cycles of garbage collecting, 
then the survivors will move to g1. There is an assumption that most 
objects have a very short life span, but those surviving a while are 
expected to survive longer. Thus objects in g1 will be garbage collected 
less frequently to save on overhead. After you garbage collect 10 times,
that is the default at least, a threshold is reached for g0 and garbage
collection happens in g1 too. Then they are moved to g1. Then when you
do garbage collection 10 times for g1 (or 100 times for g0), g2's 
garbage collection runs.
"""

import sys
import gc
import time

a = "Hello World"
print(sys.getrefcount(a))  # outputs 4

mylist = []
mylist.append(a)
print(sys.getrefcount(a))  # outputs: 5

# Since a is global, this will output the global dict which even
# contains our comments above as they are in the __doc__ entry of that
# globals dict. globals()['a'] == a
print(gc.get_referrers(a))
print(globals()['a'] == a)  # outputs: true

print(gc.get_threshold())  # outputs: (700, 10, 10)
# Change to 1000 allocations per g0, 20x g0 -> g1, 30x g1 -> g2
gc.set_threshold(1000, 20, 30)
print(gc.get_threshold())  # outputs: (1000, 20, 30)

# To see the allocations and number of g0 and g1 allocations
print(gc.get_count())
# If you want to see when garbage collection is happening
gc.set_debug(True)


"""
We are now going to cause garbage collection to happen a lot in order
to see that we can actually speed things up quite a bit by reducing
the amount of garbage collection we do.
"""
gc.set_debug(False)


class Link:
    def __init__(self, next_link, value):
        self.next_link = next_link
        self.value = value

    def __repr__(self):
        return self.value


start = time.perf_counter()
l = Link(next_link=None, value="Main Link")
for i in range(10000000):
    l_temp = Link(l, value="L")
    mylist.append(l_temp)
end = time.perf_counter()

print("threshold0: 1000, threshold1: 20, threshold2: 30")
print("Seconds:", round(end - start, 2))

gc.set_threshold(20000, 50, 100)

start = time.perf_counter()
l = Link(next_link=None, value="Main Link")
for i in range(10000000):
    l_temp = Link(l, value="L")
    mylist.append(l_temp)
end = time.perf_counter()

print("threshold0: 20000, threshold1: 50, threshold2: 100")
print("Seconds:", round(end - start, 2))


gc.disable()

start = time.perf_counter()
l = Link(next_link=None, value="Main Link")
for i in range(10000000):
    l_temp = Link(l, value="L")
    mylist.append(l_temp)
end = time.perf_counter()

print("Garbage collection disabled")
print("Seconds:", round(end - start, 2))

# Manually collect the three generations
# This will collect everything in the generation: even the counts!
# Collecting from 2 will reset the counts for g0 and g1 as well
print(gc.get_count())
gc.collect(0)
print(gc.get_count())
gc.collect(1)
print(gc.get_count())
gc.collect(2)
print(gc.get_count())

gc.enable()
