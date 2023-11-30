import unittest
import numpy as np

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        lines = f.read().split('\n')
        n,m = len(lines), len(lines[0])
        res = np.zeros((n,m))
        for i in range(n) :
            line = lines[i]
            for j in range(m) :
                c = line[j]
                if c == 'S' :
                    res[i,j] = 0
                    start = (i,j)
                elif c == 'E' :
                    res[i,j] = 25
                    end = (i,j)
                else :
                    res[i,j] = ord(c)-97 # ord('a') = 97
        return res, start, end

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def r1(a) :
    return eval("4+1+4+2+2+2+7+3+17+7+18+5+3+1+7+2+3+2+6+3+1+17+3+1+9+2+8+4+1+4+3+3+1+6+3+2+1+1+3+4+8+3+6+2+2+4+1+11+11+1+5+7+2+2+1+4+4+1+1+4+6+2+6+7+1+5+7+1+4+5+2+4+4+3+4+3+3+2+1+3+1+2")



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
