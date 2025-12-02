import os.path
import unittest
import time
import re

def line_split(line: str) :
    return tuple(map(int, line.split('-')))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split(',')))



REGEX1 = re.compile(r'^(\d+)\1$')
REGEX2 = re.compile(r'^(\d+)\1+$')

def is_invalid(id: str, regex: re.Pattern) -> bool:
    return bool(regex.match(id))

def solve(puzzle_input, regex, debug=False):
    if puzzle_input is None:
        return None
    res = 0
    invalid_ids = []
    for x in puzzle_input :
        for int_id in range(x[0], x[1] + 1):
            if (is_invalid(str(int_id), regex)):
                res += int_id
                if debug:
                    invalid_ids.append(int_id)
    if debug:
        print(f"Invalid ids: {invalid_ids}")
    return res

def r1(puzzle_input, debug=False) :
    return solve(puzzle_input, REGEX1, debug)

def r2(puzzle_input, debug=False) :
    return solve(puzzle_input, REGEX2, debug)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_invalid_ids(self):
        for int_id in (11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859):
            self.assertTrue(is_invalid(str(int_id), REGEX1))

    def test_valid_ids(self):
        # 565653-565659,824824821-824824827,2121212118-2121212124
        for int_id in range(565653, 565659):
            self.assertFalse(is_invalid(str(int_id), REGEX1))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')
    if puzzle is not None:
        print(f"Real input: [{puzzle[0]}, ..., {puzzle[-1]}]")

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
