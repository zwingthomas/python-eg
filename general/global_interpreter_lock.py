# Acknowledgements____
# Tech with Tim
# The Python Global Interpreter Lock - Explained
# https://www.youtube.com/watch?v=XVcRQ6T9RHo&list=PLFsQXEmSzyOVejqYvO-17pGc5fIFahGXf&index=13&ab_channel=TechWithTim


"""
The GIL or the Global Interpreter Lock restricts parallel processing.
In 2023 a typical CPU has four cores. These handle software threads.
Software threads handle applications. The more cores we have, the more
we can execute at the same time. In an example where we sum the 
numbers from 1 to 20, on one thread we would go about adding these
sequentially. If we used four cores we would be able to split up 
adding 5 numbers to each core and then sum the final four. However, in
Python it doesn't quite work like this.

Because your compiled Python code is interpreted only one thread can
use the interpreter at a given time. Thus if a thread is waiting it 
can release the GIL, but only one can hold the GIL at a given time. 
This is really bad as it seriously slows down any kind of parallelism 
and only allows for concurrency. So I/O bound is very well handled, 
but multiprocessing requires a module that will side step the GIL
and, while it is harder to develop than threading, it does allow you
to side-step the GIL and work on multiple cores.

"""
