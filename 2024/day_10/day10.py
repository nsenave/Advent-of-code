import os.path
import unittest
import time

import numpy as np

def line_split(line: str) :
    res = []
    for c in line:
        if c == '.' :
            res.append(99)
            continue
        res.append(int(c))
    return res

def to_array(raw_map: str) -> np.array:
    return np.array(list(map(line_split, raw_map.split('\n'))), dtype=int)

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return to_array(f.read())



def hiking_trails(topographic_map: np.array, debug=False):
    res = 0
    n, m = topographic_map.shape
    for i in range(n):
        for j in range(m):
            if topographic_map[i,j] == 0:
                reached_coords = []
                score = compute_score(topographic_map, i, j, reached_coords)
                res += score
                if debug:
                    print(f"Trailhead at {(i,j)} has a score of {score}")
    return res

def compute_score(topographic_map, i, j, reached_coords):
    if topographic_map[i,j] == 9 and (i,j) not in reached_coords:
        reached_coords.append((i,j))
        return 1
    res = 0
    if move_up(topographic_map, i, j):
        res += compute_score(topographic_map, i-1, j, reached_coords)
    if move_down(topographic_map, i, j):
        res += compute_score(topographic_map, i+1, j, reached_coords)
    if move_right(topographic_map, i, j):
        res += compute_score(topographic_map, i, j+1, reached_coords)
    if move_left(topographic_map, i, j):
        res += compute_score(topographic_map, i, j-1, reached_coords)
    return res

def move_up(topographic_map, i, j): 
    return (i > 0) and (topographic_map[i-1,j] - topographic_map[i,j] == 1)

def move_down(topographic_map, i, j): 
    return (i < topographic_map.shape[0] - 1) and (topographic_map[i+1,j] - topographic_map[i,j] == 1)

def move_right(topographic_map, i, j): 
    return (j < topographic_map.shape[1] - 1) and (topographic_map[i,j+1] - topographic_map[i,j] == 1)

def move_left(topographic_map, i, j): 
    return (j > 0) and (topographic_map[i,j-1] - topographic_map[i,j] == 1)

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    return hiking_trails(puzzle_input, debug)



def compute_rating(topographic_map, i, j):
    if topographic_map[i,j] == 9 :
        return 1
    res = 0
    if move_up(topographic_map, i, j):
        res += compute_rating(topographic_map, i-1, j)
    if move_down(topographic_map, i, j):
        res += compute_rating(topographic_map, i+1, j)
    if move_right(topographic_map, i, j):
        res += compute_rating(topographic_map, i, j+1)
    if move_left(topographic_map, i, j):
        res += compute_rating(topographic_map, i, j-1)
    return res

def hiking_trails2(topographic_map: np.array, debug=False):
    res = 0
    n, m = topographic_map.shape
    for i in range(n):
        for j in range(m):
            if topographic_map[i,j] == 0:
                rating = compute_rating(topographic_map, i, j)
                res += rating
                if debug:
                    print(f"Trailhead at {(i,j)} has a rating of {rating}")
    return res

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    return hiking_trails2(puzzle_input, debug)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.example1 = to_array("""\
0123
1234
8765
9876""")
        self.example2 = to_array("""\
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9""")
        self.example3 = to_array("""\
..90..9
...1.98
...2..7
6543456
765.987
876....
987....""")
        self.example4 = to_array("""\
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01""")
        self.example5 = to_array("""\
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....""")
        self.example6 = to_array("""\
..90..9
...1.98
...2..7
6543456
765.987
876....
987....""")
        self.example7 = to_array("""\
012345
123456
234567
345678
4.6789
56789.""")

    def test_move(self):
        self.assertTrue(move_down(self.example2, 0, 3))
        self.assertFalse(move_up(self.example2, 0, 3))

    def test(self):
        self.assertEqual(1, hiking_trails(self.example1))
        self.assertEqual(2, hiking_trails(self.example2))
        self.assertEqual(4, hiking_trails(self.example3))
        self.assertEqual(1+2, hiking_trails(self.example4))
    
    def test2(self):
        self.assertEqual(3, hiking_trails2(self.example5))
        self.assertEqual(13, hiking_trails2(self.example6))
        self.assertEqual(227, hiking_trails2(self.example7))

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
