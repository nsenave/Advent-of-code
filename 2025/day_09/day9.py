import os.path
import unittest
import time
import re

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
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

def area2(coords):
    return area(coords[0], coords[1])

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
    return max([area2(coords) for coords in list_pairs(puzzle_input)])



def arrange(puzzle_input, n, m) -> list:
    res = []
    for i in range(n):
        line = []
        for j in range(m):
            if (j, i) in puzzle_input:
                line.append("#")
            else:
                line.append(".")
        res.append(line)
    return res

def grid_to_string(grid: list) -> str:
    return '\n'.join(list(map(lambda line: ''.join(line), grid)))

def switch_tile(tile: str):
    if (tile == '.'): return 'X'
    if (tile == 'X'): return '.'
    raise ValueError(tile)

def horizontal_lines(grid, n, m):
    for i in range(n):
        line = grid[i]
        assert line.count('#') % 2 == 0
        tile = '.'
        for j in range(m):
            if line[j] == '#':
                tile = switch_tile(tile)
                continue
            if tile == 'X':
                line[j] = tile

def vertical_lines(grid, n, m):
    for j in range(m):
        red_count = 0
        tile = '.'
        for i in range(n):
            if grid[i][j] == '#':
                red_count += 1
                tile = switch_tile(tile)
                continue
            if tile == 'X':
                grid[i][j] = tile
        assert red_count % 2 == 0

def count_groups(line):
    return len(re.findall(r'\.+', ''.join(line)))

def fill(grid, n, m):
    for i in range(n):
        line = grid[i]
        dot_groups = count_groups(line)
        if dot_groups == 1 or (dot_groups % 2 == 0):
            continue
        tile = '.'
        j = 0
        while j < m:
            if line[j] != '.':
                while line[j] != '.':
                    j += 1
                tile = switch_tile(tile)
            if tile == 'X':
                line[j] = tile
            j += 1

def is_in_tiles(pair, grid):
    y1, x1 = pair[0]
    y2, x2 = pair[1]
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    for i in range(x1, x2):
        for j in range(y1, y2):
            if grid[i][j] == '.':
                return False
    return True

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None

    n = max([coords[1] for coords in puzzle_input]) + 2
    m = max([coords[0] for coords in puzzle_input]) + 3
    # Note: + 2 / + 3 to match given examples representations
    grid = arrange(puzzle_input, n, m)
    horizontal_lines(grid, n, m)
    vertical_lines(grid, n, m)
    fill(grid, n, m)
    if debug:
        print(grid_to_string(grid))
    # works for example but actual input is too large to be stored in a 2d array
    # todo: coords compression
    # https://phuongdinh1411.github.io/cses-analyses/problem_soulutions/graph_algorithms/coordinate_compression_analysis

    pairs = list_pairs(puzzle_input)
    filtered_pairs = list(filter(lambda pair: is_in_tiles(pair, grid), pairs))
    return max([area2(coords) for coords in filtered_pairs])



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
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
