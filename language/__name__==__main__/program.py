import calculator

"""
Notice when we don't use the __name__ == "__main__": in calculator.py
we get outputs from the calculator import when we run our program file.
If we use __name__ == "__main__": this does not happen as we are not
directly running the calculator file. When you import something in 
Python you RUN THE ENTIRE MODULE. This is the key take away.

__name__ will be equal to "__main__" if it is run directly. If it is 
imported then it will be equal to its import. In this case "calculator".

"""

num1 = 10
num2 = 5

print("Using the calculator module:")
print(f"The sum of {num1} and {num2} is: {calculator.add(num1, num2)}")
print(
    f"The difference between {num1} and {num2} is {calculator.subtract(num1, num2)}")
