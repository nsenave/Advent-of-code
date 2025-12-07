import os.path
import unittest
import time

def line_split(line: str) :
    return line

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))



def find_start_index(line: str):
    return line.index("S")

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    start_line = puzzle_input[0]
    beams = {find_start_index(start_line)}
    for i in range(2, len(puzzle_input), 2):
        line = puzzle_input[i]
        new_beams = set()
        for j in beams:
            if line[j] == '.':
                new_beams.add(j)
                continue
            res += 1
            new_beams.add(j - 1)
            new_beams.add(j + 1)
        beams = new_beams
    return res



def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    start_line = puzzle_input[0]
    start_index = find_start_index(start_line)
    beams = {start_index}
    stack = [0 if j != start_index else 1 for j in range(len(start_line))]
    for i in range(2, len(puzzle_input), 2):
        line = puzzle_input[i]
        new_beams = set()
        if debug:
            print(stack)
        for j in beams:
            if line[j] == '.':
                new_beams.add(j)
                continue
            new_beams.add(j - 1)
            new_beams.add(j + 1)
            value = stack[j]
            stack[j] = 0
            stack[j-1] += value
            stack[j+1] += value
        beams = new_beams
    if debug:
        print(stack)
    return sum(stack)



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
