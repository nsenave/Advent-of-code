import unittest

def line_split(line) :
    res = line
    return res

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        puzzle = list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def r1(a) :
    return None



def r2(a) :
    return None



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    # print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    # print(f"Puzzle answer:  {r2(puzzle)}")
