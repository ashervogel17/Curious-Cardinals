"""
Basic calculator program to perform addition, subtraction, multiplication, and division.

Input: "<number> <operator> <number>"
Output: result of the operator

Written by: Asher Vogel
"""
import re


print("Imported calculator functions")


def is_operator(c):
    if c == "+" or c == "-" or c == "*" or c == "/":
        return True

    return False


"""
Parameters:
    first_operand - float
    operator - string, either "+", "-", "*", or "/"
    second_operand - float
Returns:
    The result of evaluating the expression.
    
    e.g. evaluate_expression(1, "+", 1) returns 2
         evaluate_expression(5, "-", 2) returns 3
         evaluate_expression(2, "*", 4) returns 8
         evaluate_expression(6, "/", 3) returns 2

"""
def evaluate_expression(first_operand, operator, second_operand):
    # TO DO: your code here
    pass


def parse_user_input(user_input):
    user_input.strip()
    if user_input == "q":
        return None

    # add spaces in the case that numbers are right next to operators but remove double spaces
    index = 1
    while index < len(user_input):
        # operator followed by number --> add space
        if is_operator(user_input[index - 1]) and user_input[index].isnumeric():
            user_input = user_input[0:index] + " " + user_input[index:]
            index += 1
        # number followed by operator --> add space
        elif user_input[index - 1].isnumeric() and is_operator(user_input[index]):
            user_input = user_input[0:index] + " " + user_input[index:]
            index += 1
        # operator followed by operator --> invalid
        elif is_operator(user_input[index - 1]) and is_operator(user_input[index]):
            print("Cannot parse input with back-to-back operators")
            return None
        # double space --> remove one
        elif user_input[index-1].isspace() and user_input[index].isspace():
            user_input = user_input[0:index] + user_input[index+1:]
        else:
            index += 1

    # split input, validate input, and call evaluate_expression()
    token_array = re.split('\s', user_input)
    if len(token_array) != 3:
        print("Please use the format: <number> <operator> <number>")
        return None
    elif not token_array[0].isnumeric() or not token_array[2].isnumeric():
        print("Both operands must be numbers")
        return None
    elif not is_operator(token_array[1]):
        print("Only valid operator are +, -, *, /")
        return None
    else:
        return evaluate_expression(float(token_array[0]), token_array[1], float(token_array[2]))