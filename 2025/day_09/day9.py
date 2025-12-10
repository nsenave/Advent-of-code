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



# coords in input are 'inverted' (y, x)
def xy_coords(puzzle_input) -> list:
    return [(yx_coord[1], yx_coord[0]) for yx_coord in puzzle_input]

def area(pair: tuple) -> int:
    x1, y1 = pair[0]
    x2, y2 = pair[1]
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

def list_pairs(coords):
    pairs = []
    length = len(coords)
    for i in range(length):
        for j in range(i + 1, length):
            pairs.append((coords[i], coords[j]))
    return pairs

def find_max_area(pairs):
    return max([area(pair) for pair in pairs])

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    coords = xy_coords(puzzle_input) # not required for this part, but for the sake of consistency
    return find_max_area(list_pairs(coords))



def compress_coords(coords: list):
    x_values = sorted(list({coord[0] for coord in coords}))
    y_values = sorted(list({coord[1] for coord in coords}))
    x_dict = {x_values[i]: i for i in range(len(x_values))}
    y_dict = {y_values[j]: j for j in range(len(y_values))}
    compressed_coords = [(x_dict[coord[0]], y_dict[coord[1]]) for coord in coords]
    return compressed_coords, x_dict, y_dict

def decompress_coord(compressed_coord, inverted_x, inverted_y):
    i, j = compressed_coord
    return ((inverted_x[i], inverted_y[j]))

def decompress_pairs(pairs, x_dict: dict, y_dict: dict) -> tuple:
    result = []
    inverted_x = {i: x for x, i in x_dict.items()}
    inverted_y = {j: y for y, j in y_dict.items()}
    for pair in pairs:
        decompressed1 = decompress_coord(pair[0], inverted_x, inverted_y)
        decompressed2 = decompress_coord(pair[1], inverted_x, inverted_y)
        result.append((decompressed1, decompressed2))
    return result

def arrange(coords, n, m) -> list:
    res = []
    for x in range(n):
        line = []
        for y in range(m):
            if (x, y) in coords:
                line.append("#")
            else:
                line.append(".")
        res.append(line)
    return res

def grid_to_string(grid: list) -> str:
    return '\n'.join(list(map(lambda line: ''.join(line), grid)))

def connect(grid, coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    if (y1 == y2): # horizontal case
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            grid[x][y1] = 'X'
        return
    if (x1 == x2): # vertical case
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            grid[x1][y] = 'X'
        return
    raise AssertionError(f"Diagonal dots: {coord1}, {coord2}")

def top_collision(x, y, grid):
    while x >= 0 and grid[x][y] == '.':
        x -= 1
    return x != -1

def bottom_collision(x, y, grid, n):
    while x < n and grid[x][y] == '.':
        x += 1
    return x != n

def left_collision(x, y, grid):
    while y >= 0 and grid[x][y] == '.':
        y -= 1
    return y != -1

def right_collision(x, y, grid, m):
    while y < m and grid[x][y] == '.':
        y += 1
    return y != m

def is_in_shape(x, y, grid, n, m) -> bool:
    if not top_collision(x, y, grid):
        return False
    if not bottom_collision(x, y, grid, n):
        return False
    if not left_collision(x, y, grid):
        return False
    if not right_collision(x, y, grid, m):
        return False
    return True

def fill(grid, n, m):
    for x in range(n):
        for y in range(m):
            if grid[x][y] == '.':
                if is_in_shape(x, y, grid, n, m):
                    grid[x][y] = 'X'

def is_in_tiles(pair, grid) -> bool:
    x1, y1 = pair[0]
    x2, y2 = pair[1]
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if grid[x][y] == '.':
                return False
    return True

def solve(coords, debug) -> list:
    n = max([coord[0] for coord in coords]) + 2
    m = max([coord[1] for coord in coords]) + 3
    # Note: + 2 / + 3 to match given example representations
    grid = arrange(coords, n, m)
    for k in range(len(coords)):
        connect(grid, coords[k-1], coords[k])
    fill(grid, n, m)
    if debug:
        print(grid_to_string(grid))
    pairs = list_pairs(coords)
    return list(filter(lambda pair: is_in_tiles(pair, grid), pairs))

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    coords = xy_coords(puzzle_input)
    filtered_pairs = solve(coords, debug)
    return find_max_area(filtered_pairs)

def r2_with_compression(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    coords = xy_coords(puzzle_input)
    compressed_coords, x_dict, y_dict = compress_coords(coords)
    filtered_pairs = solve(compressed_coords, debug)
    return find_max_area(decompress_pairs(filtered_pairs, x_dict, y_dict))



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
    print(f"Example result (no compression): {r2(example, True)}")
    print(f"Example result (compression):    {r2_with_compression(example, True)}")
    print(f"Puzzle answer (compression):     {r2_with_compression(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
