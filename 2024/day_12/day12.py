import os.path
import unittest
import time

from copy import deepcopy

class Garden:
    def __init__(self, plots):
        self.plots = plots
        self.x_length = len(plots)
        self.y_length = len(plots[0])
    def __str__(self):
        return '\n'.join(map(lambda line: ''.join(line), self.plots))
    def get(self, i, j):
        if i < 0 or i >= self.x_length or j < 0 or j >= self.y_length:
            return '.'
        return self.plots[i][j]

def line_split(line: str) :
    return list(line)

def to_garden(raw_input):
    return Garden(list(map(line_split, raw_input.split('\n'))))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return to_garden(f.read())



def compute_area(region: Garden):
    res = 0
    for i in range(region.x_length):
        for j in range(region.y_length):
            res += region.get(i, j) != '.'
    return res

def perimeter_contibution2(i, j, region: Garden):
    res = 0
    res += region.get(i-1, j) == '.'
    res += region.get(i, j+1) == '.'
    res += region.get(i+1, j) == '.'
    res += region.get(i, j-1) == '.'
    return res

def compute_perimeter(region: Garden):
    res = 0
    for i in range(region.x_length):
        for j in range(region.y_length):
            if region.get(i, j) != '.':
                res += perimeter_contibution2(i, j, region)
    return res

def propagate(garden: Garden, i, j) :
    region = Garden([['.' for j in range(garden.y_length)] for i in range(garden.x_length)])
    plant = garden.get(i, j)
    helper(garden, region, i, j, plant)
    return region

def helper(garden: Garden, region: Garden, i, j, plant):
    garden.plots[i][j] = '.'
    region.plots[i][j] = plant
    for neighboor in ((i-1, j), (i, j+1), (i+1, j), (i, j-1)) :
        i2, j2 = neighboor
        if garden.get(i2, j2) == plant:
            helper(garden, region, i2, j2, plant)

def get_plant_type(region: Garden):
    """Used in debug"""
    for i in range(region.x_length):
        for j in range(region.y_length):
            if region.get(i, j) != '.':
                return region.get(i, j)

def compute_price(region: Garden, perimeter_function=compute_perimeter, debug=False):
    area = compute_area(region)
    perimeter = perimeter_function(region)
    price = area * perimeter
    if debug:
        print(f"A region of {get_plant_type(region)} plants with price {area} * {perimeter} = {price}.")
    return price

def compute_total_price(garden: Garden, perimeter_function=compute_perimeter, debug=False):
    res = 0
    for i in range(garden.x_length):
        for j in range(garden.y_length):
            if garden.get(i, j) != '.':
                region = propagate(garden, i, j)
                res += compute_price(region, perimeter_function, debug)
    return res

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    garden = deepcopy(puzzle_input)
    return compute_total_price(garden, debug=debug)



def up(i):
    return i - 1
def down(i):
    return i + 1
def horizontal_sides(garden: Garden, direction):
    res = 0
    for i in range(garden.x_length):
        j = 0
        while j < garden.y_length:
            if garden.get(i, j) != '.' and garden.get(direction(i), j) == '.':
                res += 1
                while j < garden.y_length and garden.get(i, j) != '.' and garden.get(direction(i), j) == '.':
                    j += 1
            j += 1
    return res

def left(j):
    return j - 1
def right(j):
    return j + 1
def vertical_sides(garden: Garden, direction):
    res = 0
    for j in range(garden.y_length):
        i = 0
        while i < garden.x_length:
            if garden.get(i, j) != '.' and garden.get(i, direction(j)) == '.':
                res += 1
                while i < garden.x_length and garden.get(i, j) != '.' and garden.get(i, direction(j)) == '.':
                    i += 1
            i += 1
    return res

def count_sides(garden):
    return horizontal_sides(garden, up) + horizontal_sides(garden, down) + \
        vertical_sides(garden, left) + vertical_sides(garden, right)

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    garden = deepcopy(puzzle_input)
    return compute_total_price(garden, perimeter_function=count_sides, debug=debug)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.example1 = to_garden("""\
AAAA
BBCD
BBCC
EEEC""")
        self.example2 = to_garden("""\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""")
        self.example3 = to_garden("""\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""")

    def test_total_price(self):
        self.assertEqual(140, compute_total_price(self.example1))
        self.assertEqual(772, compute_total_price(self.example2))

    def test_sides(self):
        e_plants = propagate(self.example3, 0, 0)
        self.assertEqual(3, horizontal_sides(e_plants, up))
        self.assertEqual(3, horizontal_sides(e_plants, down))
        self.assertEqual(1, vertical_sides(e_plants, left))
        self.assertEqual(5, vertical_sides(e_plants, right))
        self.assertEqual(12, count_sides(e_plants))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    #print("Example input:")
    #print(example)

    puzzle = parse_input('input.txt')

    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}") # 1930
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}") # 1206
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
