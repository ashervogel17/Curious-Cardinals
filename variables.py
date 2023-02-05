"""
Module: Fundamentals
Topic: Variables
"""

# Variable assignment
current_year = 2022

# Q: Behind the scenes, what does Python do here?
# A:
#   - allocates memory to store the integer 42
#   - names that place in memory current_year
#   - stores a pattern of 0's and 1's to represent 42 in that memory address

# Notice: left side is a variable name, right side is a value that we are setting the variable to

# Variable types
current_year = 2022 # integer
current_month = "December" # string
is_the_sky_blue = True # boolean
pi_approximation = 3.14 # float

# These are the 4 most commonly used variable types. Note, however, that there are more and you can even create your own! More on that later.
# Also, notice how we use '=' in code. Q: How is this different than in mathematics?

# Once data is stored in a variable, we can use that variable name to retrieve the data.
# e.g.
print(current_year)

# Q: What will this code do?
x = 2
print(x)
x = 5
print(x)

# Q: What will this code do?
x = 7
x = x + 1
print(x)

# Q: What's wrong this this line of code?
    # 3 = x

# Discussion: Importance of choosing good variable names and variable naming conventions

# Q: What is an operator? (e.g. +)
# Q: What is an expression? (e.g. x + y)
x = 5
y = 7
print(x + y)
print(x - y)
print(x * y) # we use * to avoid confusion with x
print(x / y)

# One more operator: Integer division - explain how it works
x = 12
y = 5
print(x // y)

# Introduce the string data type
example_string = "I am a string"
print(example_string)

# String concatenation
first_string = "George "
second_string = "Washington"
print(first_string + second_string)

# Printing string variables (note the difference between the following two lines of code)
print("current_month") # note: you can also use single quotes
print(current_month)

# Another example
print("2 + 6")
print(2 + 6)

# Converting between variable types
# "Cast" a variable as being of a different type with float(), int(), str(), or bool() to let it behave like it is that type
# e.g
number_of_apples = 37
print(number_of_apples)
print(float(number_of_apples))

print("As an integer: " + str(number_of_apples))
print("As a float: " + str(float(number_of_apples)))

# Q: Why use variables?
# A:
#   - resuse values
#   - use values to compute other values
#   - make it easy to change the behavior of code

# Mini exercise: write a program that takes in a subtotal and tells you how much to tip (note: demonstrate input function)
# e.g.
subtotal = input("Enter the subtotal: ")
tip = float(subtotal) / 5
print("You should tip $" + str(tip))

## Recommended exercise: Tip Calculator