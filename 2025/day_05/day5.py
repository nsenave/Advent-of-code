import os.path
import unittest
import time

def line_split(line: str) :
    return tuple(map(int, line.split('-')))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        content1, content2 = f.read().split('\n\n')
        ranges = list(map(line_split, content1.split('\n')))
        ids = list(map(int, content2.split('\n')))
        return (ranges, ids)



def is_in_range(id, lower, upper):
    return lower <= id <= upper

def is_fresh(id: int, ranges: list):
    for idRange in ranges:
        if is_in_range(id, idRange[0], idRange[1]):
            return True
    return False

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    ranges, ids = puzzle_input
    res = 0
    for id in ids :
        if is_fresh(id, ranges):
            res += 1
    return res



def range_length(idRange):
    lower, upper = idRange[0], idRange[1]
    return max(0, upper - lower + 1)

def count_fresh(resolved_ranges: list):
    """Ranges must be resolved (no intersections)."""
    return sum(map(range_length, resolved_ranges))

def update_bounds(range_a, range_b):
    lower_b = range_b[0]
    assert range_a[0] <= lower_b
    upper_a = range_a[1]
    if upper_a < lower_b:
        return
    range_b[0] = upper_a + 1

def sorted_ranges(ranges: list):
    """Sorts by lower bound."""
    return sorted(ranges, key=lambda idRange: idRange[0])

def resolve_ranges(ranges: list):
    # sorted copy with mutable lists
    resolved_ranges = [[idRange[0], idRange[1]] for idRange in sorted_ranges(ranges)]
    ranges_number = len(ranges)
    for i in range(ranges_number - 1):
        for j in range(i+1, ranges_number):
            update_bounds(resolved_ranges[i], resolved_ranges[j])
    return resolved_ranges

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    ranges = puzzle_input[0]
    resolved_ranges = resolve_ranges(ranges)
    if debug:
        print(resolved_ranges)
    return count_fresh(resolved_ranges)



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
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
