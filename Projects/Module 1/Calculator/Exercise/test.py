from student_calculator_functions import *

def float_comp(a, b):
    return abs(a - b) < 0.0001

errors = 0

outputs = []
with open("../Solution/test_outputs.txt", "r") as f:
    for line in f.readlines():
        outputs.append(float(line))

with open("../Solution/test_inputs.txt", "r") as f:
    i = 0
    for line in f.readlines():
        result = parse_user_input(line.strip())
        if result is None or result != outputs[i]:
            print("Failed on: " + line)
            errors += 1
        i += 1

if errors == 0:
    print("Passed all test cases")
else:
    print(f"Failed {errors} test cases")