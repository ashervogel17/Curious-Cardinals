"""
Module: Fundamentals
Topic: More on Functions
"""

# Functions with parameters

# Explain the syntax here:
def print_number(num):
    print(num)

# How to call it:
print_number(7)
print_number(12)

# Q: What's wrong with this line of code?
# print_number()

# Another example
def print_name(name):
    print("Hi, my name is " + name + ".")

print_name("Asher")
print_name("Jeffery")

# Calling a function from within another function:
def print_introduction(name, age):
    print_name(name)
    print("I am " + str(age) + " years old.")

# Functions that return a value - explain what is means for a function to return a value
def add_10(num):
    result = num + 10
    return result

# Introduce library functions - part of what makes Python so awesome is how many libraries people have built that you can use right out of the box!
# e.g.
from math import sqrt

print(sqrt(9))

# Introduce the concept of abstraction (i.e. building high-level code from smaller building blocks which unraveling the fine details of the buliding blocks)
# A good analogy is a gas pedal - you may not understand what goes on under the hood of the car but you know that by pressing the pedal, the car goes forward!
# Q: What are some examples of abstraction that you use in your hobbies/everyday life?