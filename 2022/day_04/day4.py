import unittest

def line_split(line) :
    return tuple(map(lambda pair: tuple(map(int, pair.split('-'))), line.split(',')))

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def overlap(pair: tuple) :
    p1, p2 = pair
    if p1[0] < p2[0] :
        return p1[1] >= p2[1]
    elif p1[0] > p2[0] :
        return p1[1] <= p2[1] 
    else :
        return True

def r1(a) :
    res = 0
    for pair in a :
        if overlap(pair) :
            res += 1
    return res



def overlap2(pair: tuple) :
    p1, p2 = pair
    if p1[0] < p2[0] :
        return p1[1] >= p2[0]
    elif p1[0] > p2[0] :
        return p2[1] >= p1[0] 
    else :
        return True

def r2(a) :
    res = 0
    for pair in a :
        if overlap2(pair) :
            res += 1
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_overlap(self):
        self.assertTrue(overlap(((1,4),(2,3))))
        self.assertTrue(overlap(((1,4),(1,4))))
        self.assertTrue(overlap(((1,4),(1,3))))
        self.assertTrue(overlap(((1,4),(2,3))))
        self.assertTrue(overlap(((2,3),(1,4))))
        self.assertTrue(overlap(((1,4),(1,4))))
        self.assertTrue(overlap(((1,3),(1,4))))
        self.assertTrue(overlap(((2,4),(1,4))))
        self.assertTrue(overlap(((5,5),(5,94))))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
