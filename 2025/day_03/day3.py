import os.path
import unittest
import time

def line_split(line: str) :
    return list(map(int, line))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))



def find_max(numbers: list) -> tuple:
    result = 0
    index = 0
    for i in range(len(numbers)):
        n = numbers[i]
        if n > result:
            result = n
            index = i
    return (result, index)

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for x in puzzle_input :
        n1, i = find_max(x[:-1])
        n2 = max(x[i+1:])
        voltage = str(n1) + str(n2)
        if debug:
            print(f"Line voltage {voltage}")
        res += int(voltage)
    return res



def copy_list(numbers: list) -> list:
    return [n for n in numbers]

def find_max2(numbers: list, right_border: int) -> tuple:
    result = 0
    index = 0
    for i in range(len(numbers) - right_border):
        n = numbers[i]
        if n > result:
            result = n
            index = i
    for i in range(0, index + 1):
        numbers[i] = 0
    return result

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for x in puzzle_input :
        numbers = copy_list(x)
        voltage = ''
        for right_border in reversed(range(0, 12)):
            if debug:
                print(numbers)
            n = find_max2(numbers, right_border)
            voltage += str(n)
        if debug:
            print(f"Line voltage {voltage}")
        res += int(voltage)
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')

    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
