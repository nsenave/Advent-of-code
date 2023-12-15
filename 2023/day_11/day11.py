import os.path
import unittest
import numpy as np

def line_split(line: str) :
    return list(line)

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

def print_image(image: list):
    print('\n'.join(list(map(lambda row: ''.join(row), image))))

print("Example input:")
print_image(example)

def count_galaxies(image: list) -> int:
    res = 0
    for row in image:
        for pixel in row:
            if pixel == '#':
                res += 1
    return res

print(f"Number of galaxies in example: {count_galaxies(example)}")
print(f"Number of galaxies in puzzle:  {count_galaxies(puzzle)}")



def is_empty(row: list) -> bool:
    for pixel in row:
        if pixel == '#':
            return False
    return True

def is_empty_column(image: list, j: int) -> bool:
    for i in range(len(image)):
        if image[i][j] == '#':
            return False
    return True

def compute_distances(image: list) -> np.array:
    n, m = len(image), len(image[0])
    distances = np.ones((n, m), dtype=int)
    for i in range(n):
        row = image[i]
        if is_empty(row):
            for j in range(m):
                distances[i, j] = 2
    for j in range(m):
        if is_empty_column(image, j):
            for i in range(n):
                distances[i, j] = 2
    return distances

def find_galaxy_coords(image: list) -> list:
    n, m = len(image), len(image[0])
    res = []
    for i in range(n):
        for j in range(m):
            if image[i][j] == '#':
                res.append((i, j))
    return res

class Distance:

    def __init__(self) -> None:
        self.long_distance = 0
        self.short_distance = 0
    
    def __str__(self) -> str:
        return f"Distance({self.long_distance}, {self.short_distance})"
    
    def __repr__(self) -> str:
        return str(self)
    
    def add_value(self, value: int):
        if value == 1:
            self.short_distance += 1
        else:
            self.long_distance += 1
    
    def int_value(self, long_value: int) -> int:
        return self.long_distance*long_value + self.short_distance

def sum_distances(distance1: Distance, distance2: Distance) -> Distance:
    res = Distance()
    res.long_distance = distance1.long_distance + distance2.long_distance
    res.short_distance = distance1.short_distance + distance2.short_distance
    return res

# no matter which path is taken this way (galaxies are not in a long distance row/column)
def distance_between(coords1: tuple, coords2: tuple, distances: np.array) -> Distance:
    x1, y1 = coords1
    x2, y2 = coords2
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    dist = Distance()
    for x in range(x_min, x_max):
        dist.add_value(distances[x+1, y_min])
    for y in range(y_min, y_max):
        dist.add_value(distances[x_max, y+1])
    return dist

def sum_distances_between_galaxies(distances: np.array, galaxy_coords: list) -> Distance:
    result = Distance()
    galaxy_count = len(galaxy_coords)
    for k1 in range(galaxy_count):
        coords1 = galaxy_coords[k1]
        for k2 in range(k1 + 1, galaxy_count):
            coords2 = galaxy_coords[k2]
            result = sum_distances(result, distance_between(coords1, coords2, distances))
    return result

def compute_result(image) -> Distance:
    if image is None :
        return None
    distances = compute_distances(image)
    galaxy_coords = find_galaxy_coords(image)
    #print(distances)
    return sum_distances_between_galaxies(distances, galaxy_coords)

def r1(result: Distance) -> int:
    if result is None:
        return None
    return result.int_value(2)



# no real need for this but could be useful with much larger numbers
def millions_and_units_number(millions: int, units: int) -> str:
    if units >= 1000000:
        return str(millions + int(str(units)[:-6])) + str(units)[-6:]
    return str(millions) + ''.join(['0' for _ in range(6-len(str(units)))]) + str(units)

def r2(result: Distance) -> str:
    if result is None:
        return None
    print(result) 
    return millions_and_units_number(millions=result.long_distance, units=result.short_distance)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.distances = compute_distances(example)
        self.galaxy_coords = find_galaxy_coords(example)
        # Position of some galaxies in the original (not resized) grid:
        self.coords5 = (5, 1)
        self.coords9 = (9, 4)
        self.coords1 = (0, 3)
        self.coords7 = (8, 7)
        self.coords3 = (2, 0)
        self.coords6 = (6, 9)
        # Result distance object with the example
        self.result = sum_distances_between_galaxies(self.distances, self.galaxy_coords)

    def test_galaxy_coords(self):
        self.assertEqual(9, len(self.galaxy_coords))
        self.assertTrue(self.coords1 in self.galaxy_coords)
        self.assertTrue(self.coords3 in self.galaxy_coords)
        self.assertTrue(self.coords5 in self.galaxy_coords)
        self.assertTrue(self.coords6 in self.galaxy_coords)
        self.assertTrue(self.coords7 in self.galaxy_coords)
        self.assertTrue(self.coords9 in self.galaxy_coords)
    
    def test_distance_function(self):
        self.assertEqual(9, distance_between(self.coords5, self.coords9, self.distances).int_value(2))
        self.assertEqual(15, distance_between(self.coords1, self.coords7, self.distances).int_value(2))
        self.assertEqual(17, distance_between(self.coords3, self.coords6, self.distances).int_value(2))
    
    def test_result_with_larger_distances(self):
        self.assertEqual(1030, self.result.int_value(10))
        self.assertEqual(8410, self.result.int_value(100))
    
    def test_millions_and_units_number(self):
        self.assertEqual('1000001', millions_and_units_number(1, 1))
        self.assertEqual('10000000', millions_and_units_number(9, 1000000))



if __name__ == '__main__':
    unittest.main(exit=False)

    example_result = compute_result(example)
    puzzle_result = compute_result(puzzle)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example_result)}")
    print(f"Puzzle answer:  {r1(puzzle_result)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example_result)}")
    print(f"Puzzle answer:  {r2(puzzle_result)}")
