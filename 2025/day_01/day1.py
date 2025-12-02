import os.path
import unittest
import time

def line_split(line: str) :
    return (line[0], int(line[1:]))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))



def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    current = 50
    for x in puzzle_input :
        direction, value = x
        if (direction == 'L'):
            current -= value
        if (direction == 'R'):
            current += value
        current %= 100
        if current == 0:
            res += 1
    print(f"Final position: {current}")
    return res



def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    current = 50
    for x in puzzle_input :
        direction, value = x
        if (direction == 'L'):
            while value > 0:
                current -= 1
                value -= 1
                current %= 100
                if current == 0:
                    res += 1
        if (direction == 'R'):
            while value > 0:
                current += 1
                value -= 1
                current %= 100
                if current == 0:
                    res += 1
    print(f"Final position: {current}")
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
