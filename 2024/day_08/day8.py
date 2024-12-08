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



class AntinodeMap:
    def __init__(self, area: list):
        self.x_length = len(area)
        self.y_length = len(area[0])
        self.area = [['.' for j in range(self.y_length)] for i in range(self.x_length)]
    def __str__(self):
        return '\n'.join(map(lambda line: ''.join(line), self.area)) + '\n'
    def set_antinode_ij(self, i: int, j: int) :
        if i < 0 or j < 0 or i >= self.x_length or j >= self.y_length:
            return
        self.area[i][j] = '#'
    def set_antinode(self, coords: tuple) :
        i, j  = coords
        self.set_antinode_ij(i, j)
    def count_antinodes(self):
        res = 0
        for i in range(self.x_length):
            for j in range(self.y_length):
                if self.area[i][j] == '#':
                    res += 1
        return res

def show_area(area):
    print('\n'.join(area) + '\n')

def distinct_antennas(area: list):
    res = set()
    for i in range(len(area)):
        for j in range(len(area[0])):
            location = area[i][j]
            if location != '.':
                res.add(location)
    return res

def count_antenna(antenna: str, area: list):
    count = 0
    for i in range(len(area)):
        for j in range(len(area[0])):
            if antenna == area[i][j]:
                count += 1
    return count

def count_antennas(antennas: set, area: list):
    res = {}
    max_count, max_antenna = 0, None
    for antenna in antennas:
        count = count_antenna(antenna, area)
        res[antenna] = count
        if count > max_count:
            max_count, max_antenna = count, antenna
    print(f"The antenna {max_antenna} has the most occurrences: {max_count}")
    return res

def find_antenna_coords(antenna: str, area: list):
    res = []
    for i in range(len(area)):
        for j in range(len(area[0])):
            if antenna == area[i][j]:
                res.append((i,j))
    return res

def compute_antinodes(coords: list, harmonics: int):
    res = []
    n = len(coords)
    for i in range(n):
        for i2 in range(i+1, n):
            for antinode_coord in coords_reflection(coords[i], coords[i2], harmonics):
                res.append(antinode_coord)
    return res

def coords_reflection(coord1: tuple, coord2: tuple, harmonics: int):
    res = []
    i1, j1 = coord1
    i2, j2 = coord2
    delta_i = i2 - i1
    delta_j = j2 - j1
    for harmonic in range(1, harmonics + 1):
        res.append((i1 - delta_i*harmonic, j1 - delta_j*harmonic))
        res.append((i2 + delta_i*harmonic, j2 + delta_j*harmonic))
    return res

def put_antinodes(antinodeMap: AntinodeMap, area: list, antennas: list, harmonics=1, debug=False):
    for antenna in antennas:
        coords = find_antenna_coords(antenna, area)
        if debug:
            print(f"Coords of antenna '{antenna}': {coords}")
        antinodes = compute_antinodes(coords, harmonics)
        for antinode in antinodes:
            antinodeMap.set_antinode(antinode)
    if debug:
        print(antinodeMap)

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    antinodeMap = AntinodeMap(puzzle_input)
    antennas = distinct_antennas(puzzle_input)
    print(antennas)
    antenna_counts = count_antennas(antennas, puzzle_input)
    if debug:
        print(antenna_counts)

    put_antinodes(antinodeMap, puzzle_input, antennas, debug=debug)

    return antinodeMap.count_antinodes()



def intersections(antenna: str, area: list, antinodeMap: AntinodeMap):
    already_counted = 0
    coords = find_antenna_coords(antenna, area)
    for coord in coords:
        i,j = coord
        if antinodeMap.area[i][j] == '#':
            already_counted += 1
    return len(coords) - already_counted

def extra_antinodes(antennas: list, area: list, antinodeMap: AntinodeMap):
    res = 0
    for antenna in antennas:
        res += intersections(antenna, area, antinodeMap)
    return res

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    antinodeMap = AntinodeMap(puzzle_input)
    antennas = distinct_antennas(puzzle_input)

    # (Harmonics must be high enough for the case where two antennas are next to each other)
    harmonics = max(antinodeMap.x_length, antinodeMap.y_length)
    put_antinodes(antinodeMap, puzzle_input, antennas, harmonics, debug)

    antinodes_count = antinodeMap.count_antinodes()
    extra_count = extra_antinodes(antennas, puzzle_input, antinodeMap)
    print(f"Antinodes and harmonics:  {antinodes_count}")
    print(f"Extra intersection nodes: {extra_count}")
    return antinodes_count + extra_count



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual([(-1, 0), (5, 3)], coords_reflection((1,1), (2,3)))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)
    show_area(example)

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
