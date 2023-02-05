def add(num1, num2):
    return num1 + num2

num1 = input("Enter the first number: ")
num2 = input("Enter the second number: ")

result = add(int(num1), int(num2))

print(num1 + " + " + num2 + " = " + str(result))