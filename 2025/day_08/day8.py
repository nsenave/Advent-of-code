import os.path
import unittest
import time
import math

def line_split(line: str) :
    return tuple(map(int, line.split(',')))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))



def distance2(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return (z2 - z1)**2 + (y2 - y1)**2 + (x2 - x1)**2

def list_pairs(points):
    points_number = len(points)
    pairs = []
    for i in range(points_number):
        for j in range(i + 1, points_number):
            pairs.append((i, j))
    assert len(pairs) == (points_number * (points_number-1)) // 2
    return pairs

# Efficiently merging sets is not so easy, yet there's a known solution for this:
# Disjoint Set (Union-Find Data Structure)
# https://en.wikipedia.org/wiki/Disjoint-set_data_structure

# find
def find_root(circuits, i):
    if circuits[i] != i:
        return find_root(circuits, circuits[i])
    return circuits[i]

# union
def connect_points(circuits, sizes, i, j):
    root1, root2 = find_root(circuits, i), find_root(circuits, j)
    circuits[i] = root1
    circuits[j] = root2
    if root1 == root2:
        return
    circuits[root2] = root1
    sizes[root1] += sizes[root2]
    sizes[root2] = 0
    return sizes[root1] # return value added for part 2

def r1(points, n, debug=False) :
    if points is None:
        return None
    # Note: kd trees exist to find nearest neighbours in apparently O(n log n).
    # Yet, here a sort is efficient enough.
    pairs = list_pairs(points)
    pairs.sort(key=lambda pair: distance2(points[pair[0]], points[pair[1]]))
    points_number = len(points)
    circuits = {i: i for i in range(points_number)}
    sizes = {i: 1 for i in range(points_number)}
    for k in range(n):
        i, j = pairs[k]
        if debug:
            print(f"Closest points: {points[i]} and {points[j]}")
        connect_points(circuits, sizes, i, j)
    circuit_lengths = sorted(sizes.values(), reverse=True)
    if debug:
        print(circuit_lengths)
    return math.prod(circuit_lengths[:3])



def r2(points, debug=False) :
    if points is None:
        return None
    pairs = list_pairs(points)
    pairs.sort(key=lambda pair: distance2(points[pair[0]], points[pair[1]]))
    points_number = len(points)
    circuits = {i: i for i in range(points_number)}
    sizes = {i: 1 for i in range(points_number)}
    for k in range(len(pairs)):
        i, j = pairs[k]
        size = connect_points(circuits, sizes, i, j)
        if (size == points_number):
            point1, point2 = points[i], points[j]
            if debug:
                print(f"{point1}, {point2}")
            return point1[0] * point2[0]
    raise Exception("Something went wrong")



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
    print(f"Example result: {r1(example, 10, True)}")
    print(f"Puzzle answer:  {r1(puzzle, 1000)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
