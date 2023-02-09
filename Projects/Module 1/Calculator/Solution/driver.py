from calculator_functions import *

def main():
    user_input = ""
    while user_input != "q":
        # read user input, strip whitespace, and look for quit message
        user_input = input("enter calculation (q to exit): ")
        res = parse_user_input(user_input)
        if not res is None:
            print(res)

if __name__ == "__main__":
    main()