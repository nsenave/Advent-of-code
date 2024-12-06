import os.path
import unittest

def line_split(line: str) :
    return tuple(map(int, line.split("   ")))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def r1(a, debug=False) :
    res = 0
    left = []
    right = []
    for c in a:
        left.append(c[0])
        right.append(c[1])
    left.sort()
    right.sort()
    for k in range(len(a)):
        res += abs(left[k] - right[k])
    return res



def r2(a, debug=False) :
    res = 0
    left = []
    right = []
    for c in a:
        left.append(c[0])
        right.append(c[1])
    for k in range(len(a)):
        res += left[k] * right.count(left[k])
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
