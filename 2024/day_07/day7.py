import os.path
import unittest
import time

def line_split(line: str) :
    value_string, numbers_string = line.split(": ")
    return int(value_string), tuple(map(int, numbers_string.split(" ")))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def longest_equation(equations):
    longest = 0
    for equation in equations:
        length = len(equation[1])
        if length > longest:
            longest = length
    return longest

def helper(prefix, length, combinations):
    """Helper recursive function for the operator combinations computation."""
    if length == 0:
        combinations.append(prefix)
        return
    if OPERATORS is None:
        raise ValueError("Global list 'OPERATORS' not defined.")
    for operator in OPERATORS:
        helper(prefix + operator, length - 1, combinations)

def compute_operator_combinations(length: int):
    # safety measures
    if length > 12:
        raise ValueError("'Large' number, probably unintended")
    if length < 1:
        raise ValueError("Less than 1, probably unintended")
    #
    combinations = []
    helper("", length, combinations)
    return combinations

def all_combinations(max_length: int) -> dict:
    combinations_dict = {}
    for length in range (1, max_length):
        combinations_dict[length] = compute_operator_combinations(length)
    return combinations_dict

def evaluate(numbers: list, operators: str):
    res = numbers[0]
    for i in range(len(numbers) - 1):
        operator = operators[i]
        if (operator == '+'):
            res += numbers[i+1]
            continue
        if (operator == '*'):
            res *= numbers[i+1]
            continue
        if (operator == '|'):
            res = int(str(res) + str(numbers[i+1]))
            continue
        raise ValueError(f"Unexpected operator: {operator}")
    return res

def has_solution(equation, combinations):
    value, numbers = equation
    for combination in combinations:
        if evaluate(numbers, combination) == value:
            return True
    return False

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    longest = longest_equation(puzzle_input)
    print(f"Longest equation in input has {longest} numbers.")
    # => longest in input has 12 that means max combinations of operators + and * is 11^2 = 2028
    # (which is fine)
    combinations_dict = all_combinations(longest)
    if debug:
        print(combinations_dict)
    res = 0
    for equation in puzzle_input :
        value, numbers = equation
        combinations = combinations_dict[len(numbers) - 1]
        if has_solution(equation, combinations):
            res += value
    return res



def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    longest = longest_equation(puzzle_input)
    # 3^11 = 177 147, not sure it's still fine
    combinations_dict = all_combinations(longest)
    print("Finished computation of operator combinations.")
    if debug:
        print(combinations_dict)
    res = 0
    counter, equations_count = 0, len(puzzle_input)
    for equation in puzzle_input :
        value, numbers = equation
        combinations = combinations_dict[len(numbers) - 1]
        if has_solution(equation, combinations):
            res += value
        counter += 1
        if (counter%100 == 0):
            print(f"{counter} of {equations_count} equations tested.")
    # it worked
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(evaluate((1,1), "+"), 2)

if __name__ == '__main__':
    unittest.main(exit=False)


    print("--- Part One ---")

    OPERATORS = ['+', '*']

    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")


    print("--- Part Two ---")

    OPERATORS = ['+', '*', '|']

    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
