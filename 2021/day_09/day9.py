import unittest
import numpy as np

def line_split(line) :
    return [10] + list(map(int,list(line))) + [10]

def parse_input(path) :
    with open(path, 'r') as f :
        res = list(map(line_split, f.read().split('\n')))
        # add border lines to make it simpler
        m = len(res[0])
        res = [[10]*m] + res + [[10]*m]
    return np.array(res)

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def r1(a) :
    res = 0
    n,m = a.shape
    for i in range(1, n-1) :
        for j in range(1, m-1) :
            x = a[i,j]
            if x<a[i-1,j] and x<a[i+1,j] and x<a[i,j-1] and x<a[i,j+1] :
                res += x+1
    return res



def low_point_coords(a) :
    res = []
    n,m = a.shape
    for i in range(1, n-1) :
        for j in range(1, m-1) :
            x = a[i,j]
            if x<a[i-1,j] and x<a[i+1,j] and x<a[i,j-1] and x<a[i,j+1] :
                res.append((i,j))
    return res

def basin_coords(a,i,j,coords=[]) :

    def f(i,j,coords) :
        return basin_coords(a,i,j,coords)
    
    n,m = a.shape
    x = a[i,j]
    #
    adjacents = []
    if i != 0 : adjacents.append((i-1,j))
    if j != 0 : adjacents.append((i,j-1))
    if i != n : adjacents.append((i+1,j))
    if j != m : adjacents.append((i,j+1))
    for adj in adjacents :
        i2,j2 = adj
        if x<a[i2,j2] and a[i2,j2]<9:
            if adj not in coords :
                coords.append(adj)
            f(i2,j2,coords)
    return coords
    
def r2(a) :
    basin_sizes = []
    arr = np.copy(a)
    low_points = low_point_coords(a)
    for coord in low_points :
        i,j = coord
        basin = basin_coords(a,i,j,[coord])
        basin_sizes.append(len(basin))
    #
    res = 1
    for k in range(3) :
        res *= basin_sizes.pop(basin_sizes.index(max(basin_sizes)))
    return res



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
