import unittest
import numpy as np

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        lines = f.read().split('\n')
        n,m = len(lines), len(lines[0])
        res = np.zeros((n,m), dtype=int)
        for i in range(n) :
            for j in range(m) :
                res[i,j] = lines[i][j]
        return res

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def visible(grid, i, j) :
    height = grid[i,j]
    if (height > grid[i,:j]).all() :
        return True
    if (height > grid[:i,j]).all() :
        return True
    if (height > grid[i,j+1:]).all() :
        return True
    if (height > grid[i+1:,j]).all() :
        return True
    return False

def r1(grid) :
    n,m = grid.shape
    res = (n+m-2)*2
    for i in range(1, n-1) :
        for j in range(1, m-1) :
            if visible(grid, i, j) :
                res += 1
    return res



def top_score(grid, i, j) :
    height = grid[i,j]
    res = 1
    i2 = i-1
    while grid[i2,j] < height and i2 > 0 :
        res += 1
        i2 -= 1;
    return res

def bottom_score(grid, i, j) :
    height = grid[i,j]
    res = 1
    i2 = i+1
    while grid[i2,j] < height and i2 < grid.shape[0] - 1 :
        res += 1
        i2 += 1;
    return res

def left_score(grid, i, j) :
    height = grid[i,j]
    res = 1
    j2 = j-1
    while grid[i,j2] < height and j2 > 0 :
        res += 1
        j2 -= 1;
    return res

def right_score(grid, i, j) :
    height = grid[i,j]
    res = 1
    j2 = j+1
    while grid[i,j2] < height and j2 < grid.shape[1] - 1 :
        res += 1
        j2 += 1;
    return res

def scenic_score(grid, i, j) :
    return top_score(grid, i, j) * bottom_score(grid, i, j) * left_score(grid, i, j) * right_score(grid, i, j)

def r2(grid) :
    n,m = grid.shape
    res = 0
    for i in range(1, n-1) :
        for j in range(1, m-1) :
            s = scenic_score(grid, i, j)
            if s > res :
                res = s
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_top_score(self):
        self.assertEqual(4, top_score(example, 4,3))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
