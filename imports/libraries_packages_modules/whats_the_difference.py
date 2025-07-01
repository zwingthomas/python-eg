# Acknowledgements
# NeuralNine
# Modules, Packages, Libraries - What's The Difference?
# https://www.youtube.com/watch?v=GUXxLy68EF8&ab_channel=NeuralNine

"""
When you use pip, you are usually installing a python package. But it
may also be a library. Most people use these words interchangably.

A module is a python file with some functionality
A package contains multiple modules
A library contains multiple modules and packages
Generally a framework contains many libraries
 

This file running all of them is considered the 'script'.
"""

from library import package2
from library.package2 import module1
from library.package2.module1 import myfunction1, myfunction2, myfunction3

print(f"{myfunction1()} {myfunction2()}{myfunction3()}")
print(f"{module1.myfunction1()} {module1.myfunction2()}{module1.myfunction3()}")
print(f"{package2.module1.myfunction1()} {package2.module1.myfunction2()}{module1.myfunction3()}")
