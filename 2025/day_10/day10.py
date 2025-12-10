import os.path
import unittest
import time

def parse_button(str_button):
    return tuple(map(int, str_button[1:-1].split(',')))

def line_split(line: str) -> tuple:
    parts = line.split(' ')
    indicator_lights = parts[0][1:-1]
    buttons = list(map(parse_button, parts[1:-1]))
    joltages = list(map(int, parts[-1][1:-1].split(',')))
    return (indicator_lights, buttons, joltages)

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
    for x in puzzle_input :
        pass
    return res



def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for x in puzzle_input :
        pass
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
    #print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
