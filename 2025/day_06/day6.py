import os.path
import unittest
import time
import re

def line_split(line: str) :
    return list(map(int, re.split(r'\s+', line.strip())))

def parse_signs(line: str) :
    return [c for c in line if c != ' ']

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        lines = f.read().split('\n')
        return list(map(line_split, lines[:-1])), parse_signs(lines[-1])



def product(numbers):
    res = 1
    for n in numbers:
        res *= n
    return res

def transpose(number_lines):
    transposed = []
    n_columns, n_lines = len(number_lines), len(number_lines[0])
    for i in range(n_lines):
        transposed.append([])
    for i in range(n_lines):
        for j in range(n_columns):
            transposed[i].append(number_lines[j][i])
    return transposed

def compute_column(number_column, sign):
    if not number_column: # is empty
        return 0
    if sign == '+':
        return sum(number_column)
    elif sign == '*':
        return product(number_column)
    else:
        raise ValueError(sign)

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    number_lines, signs = puzzle_input
    numbers_columns = transpose(number_lines)
    if debug:
        print(numbers_columns)
    res = 0
    for number_column, sign in zip(numbers_columns, signs):
        res += compute_column(number_column, sign)
    return res



def parse_input2(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        # add an extra space for last column
        return list(map(lambda s: s + ' ', f.read().split('\n')))

def determine_bloc_width(str_signs: str, j: int, n_columns: int):
    res = 0
    while j+1 < n_columns and str_signs[j+1] == ' ':
        res += 1
        j += 1
    return res

def read_column_number(puzzle_input, j, n_lines):
    str_number = ''
    for i in range(n_lines):
        digit = puzzle_input[i][j]
        if digit != ' ':
            str_number += digit
    assert str_number != '', "Empty colmun"
    return int(str_number)

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    n_columns = len(puzzle_input[0])
    n_lines = len(puzzle_input) - 1 # don't count last element (string signs)
    str_signs = puzzle_input[-1]
    j_bloc = 0
    while j_bloc < n_columns:
        width = determine_bloc_width(str_signs, j_bloc, n_columns)
        sign = str_signs[j_bloc]
        numbers = []
        for j in range(j_bloc, j_bloc + width):
            numbers.append(read_column_number(puzzle_input, j, n_lines))
        if debug:
            print(numbers, sign)
        res += compute_column(numbers, sign)
        j_bloc += width + 1
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)

    print("--- Part One ---")

    t0 = time.time()
    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)
    puzzle = parse_input('input.txt')

    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one parsed and computed in {t1 - t0} seconds.")

    print("--- Part Two ---")

    t0 = time.time()
    example = parse_input2('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input2('input.txt')
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two parsed and computed in {t1 - t0} seconds.")
