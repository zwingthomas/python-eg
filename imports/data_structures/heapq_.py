"""
A priority queue is a data structure that orders elements by priority.

A heap will always have the lowest value in the next position on the 
heap. You can then process this highest order element and get the next
highest order element.

A heap is a tree structure that implements a Priority Queue.
"""

import heapq

# Unstructured, unordered data
data = [20, 43, 1, 17, 42, 65, 2, 55]

"""
Why not just sort?

The entry and the exit to and from the heap is O(log(n)), thus if you 
are going over the elements repeatedly, adding and removing from the
list. It is substantially more efficient to use a heap.
"""

print(data)
heapq.heapify(data)
print(data)

print(heapq.heappop(data))
print(heapq.heappop(data))
print(heapq.heappop(data))
print(data)
heapq.heappush(data, 2)
print(data)
print(heapq.heappop(data))
