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
    print('\n'.join(map(lambda line: ''.join(map(str, line)), puzzle_input)))



def neighbour_coords(x, y):
    return [(x-1, y-1), (x-1, y), (x-1, y+1), \
            (x, y-1), (x, y+1), \
            (x+1, y-1), (x+1, y), (x+1, y+1)]

def count_neighbours(rolls, x, y):
    res = 0
    for i, j in neighbour_coords(x, y):
        if rolls[i][j] == '@':
            res += 1
    return res

def r1(rolls, debug=False) :
    if rolls is None:
        return None
    res = 0
    height, width = len(rolls), len(rolls[0])
    #accessible = [[0 for _ in range(width)] for _ in range(height)]
    for x in range(1, height - 1):
        for y in range(1, width - 1):
            if (rolls[x][y] == '.'):
                continue
            if (count_neighbours(rolls, x, y) < 4):
                res += 1
                #accessible[x][y] = 1
    #return sum(map(lambda line: sum(line), accessible))
    return res



def remove_rolls(rolls, height, width):
    removed = 0
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
    height, width = len(rolls), len(rolls[0])
    removed = remove_rolls(rolls, height, width)
    while removed > 0:
        res += removed
        removed = remove_rolls(rolls, height, width)
    return res

def update_neighbours(neighbour_map, x, y):
    for i, j in neighbour_coords(x, y):
        current = neighbour_map[i][j]
        if current > 0:
            neighbour_map[i][j] = current - 1

def remove_rolls_bis(rolls, neighbour_map, height, width):
    removed = 0
    for x in range(1, height - 1):
        for y in range(1, width - 1):
            if (rolls[x][y] == '.'):
                continue
            if (neighbour_map[x][y] < 4):
                rolls[x][y] = '.'
                removed += 1
                update_neighbours(neighbour_map, x, y)
    return removed

def compute_neighbour_map(rolls, height, width) -> list:
    neighbour_map = [[0 for _ in range(width)] for _ in range(height)]
    for x in range(1, height - 1):
        for y in range(1, width - 1):
            if rolls[x][y] == '@':
                neighbour_map[x][y] = count_neighbours(rolls, x, y)
    return neighbour_map

def r2_bis(rolls, debug=False) :
    if rolls is None:
        return None
    res = 0
    height, width = len(rolls), len(rolls[0])
    neighbour_map = compute_neighbour_map(rolls, height, width)
    removed = remove_rolls_bis(rolls, neighbour_map, height, width)
    while removed > 0:
        res += removed
        removed = remove_rolls_bis(rolls, neighbour_map, height, width)
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
    print(f"Example result:     {r2(example, True)}")
    example = parse_input('input-example.txt')
    print(f"Example result bis: {r2_bis(example, True)}")

    t0 = time.time()
    print(f"Puzzle answer: {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two (method 1) computed in {t1 - t0} seconds.")

    puzzle = parse_input('input.txt')
    t0 = time.time()
    print(f"Puzzle answer: {r2_bis(puzzle)}")
    t1 = time.time()
    print(f"Part two (method 2) computed in {t1 - t0} seconds.")
