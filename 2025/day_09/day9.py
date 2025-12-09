import os.path
import unittest
import time

def line_split(line: str) :
    return tuple(map(int, line.split(',')))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))



def area(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x2 - x1) * abs(y2 - y1)

def area2(coords):
    x1, y1 = coords[0]
    x2, y2 = coords[1]
    return abs(x2 - x1) * abs(y2 - y1)

def list_pairs(points):
    pairs = []
    points_count = len(points)
    for i in range(points_count):
        for j in range(i + 1, points_count):
            pairs.append((points[i], points[j]))
    return pairs

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    pairs = list_pairs(puzzle_input)
    pairs.sort(key=lambda pair: area(pair[0], pair[1]))
    areas = [area2(coords) for coords in pairs]
    print(pairs)
    print(areas)
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
