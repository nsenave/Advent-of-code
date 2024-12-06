import os.path
import unittest

def line_split(line: str) :
    return list(map(int, line.split(" ")))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def compare_increasing(n1: int, n2: int) :
    return n2 > n1

def compare_decreasing(n1: int, n2: int) :
    return n2 < n1 

def is_safe(report: str):
    if (report[0] < report[1]):
        compare_function = compare_increasing
    else:
        compare_function = compare_decreasing
    for k in range(len(report) - 1) :
        n1, n2 = report[k], report[k+1]
        diff = abs(n2 - n1)
        if diff == 0 or diff > 3 or not compare_function(n1, n2) :
            return False
    return True

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for report in puzzle_input :
        res += is_safe(report)
    return res



def shortened_reports(report):
    reports = []
    length = len(report)
    for k in range (length):
        shortened = []
        for k2 in range(length):
            if k2 != k:
                shortened.append(report[k2])
        reports.append(shortened)
    return reports

def is_any_safe(reports):
    for report in reports:
        if is_safe(report):
            return True
    return False

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for report in puzzle_input :
        reports = shortened_reports(report)
        if debug:
            print(reports)
        res += is_any_safe(reports)
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
