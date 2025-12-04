import os.path
import unittest
import time

def line_split(line: str) :
    return list('.' + line + '.')

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        result = list(map(line_split, f.read().split('\n')))
        width = len(result[0])
        result.insert(0, ['.' for _ in range(width)])
        result.append(['.' for _ in range(width)])
        return result

def pretty_print(puzzle_input):
    print('\n'.join(map(lambda line: ''.join(line), puzzle_input)))



def count_neighbours(rolls, x, y):
    res = 0
    for i in (x-1, x, x+1):
        for j in (y-1, y, y+1):
            if rolls[i][j] == '@':
                res += 1
    return res - 1

def r1(rolls, debug=False) :
    if rolls is None:
        return None
    res = 0
    height, width = len(rolls), len(rolls[0])
    #accessible = [[0 for j in range(width)] for i in range(height)]
    for x in range(1, height - 1):
        for y in range(1, width - 1):
            if (rolls[x][y] == '.'):
                continue
            if (count_neighbours(rolls, x, y) < 4):
                res += 1
                #accessible[x][y] = 1
    #return sum(map(lambda line: sum(line), accessible))
    return res



def remove_rolls(rolls):
    removed = 0
    height, width = len(rolls), len(rolls[0])
    for x in range(1, height - 1):
        for y in range(1, width - 1):
            if (rolls[x][y] == '.'):
                continue
            if (count_neighbours(rolls, x, y) < 4):
                rolls[x][y] = '.'
                removed += 1
    return removed

def r2(rolls, debug=False) :
    if rolls is None:
        return None
    res = 0
    removed = remove_rolls(rolls)
    while removed > 0:
        res += removed
        removed = remove_rolls(rolls)
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
    print("Pretty print:")
    pretty_print(example)

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
