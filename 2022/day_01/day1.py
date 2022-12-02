import unittest

def line_split(line) :
    res = int(line) if line != '' else -1
    return res

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def r1(a) :
    inventories = []
    current = 0
    for c in a :
        if c == -1 :
            inventories.append(current)
            current = 0
        else :
            current += c
    inventories.sort()
    return inventories[-1]



def r2(a) :
    inventories = []
    current = 0
    for c in a :
        if c == -1 :
            inventories.append(current)
            current = 0
        else :
            current += c
    inventories.sort()
    return sum(inventories[-3:])



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
