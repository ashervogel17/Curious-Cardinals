"""
Module: Fundamentals
Topic: Input
"""

# Motivation: many interesting programming applications require interacting with the user. The easiest way to get input from a user is with the input() function.
num = input("Give me a number: ") # store the input in a variable called num
print(num)

# Important point: input always returns a string, even if that string is something like '7'

# Mini exercise: write a program that asks the user for a word and then prints it out three times
# e.g.
word = input("Pick a word: ")
print(word)
print(word)
print(word)