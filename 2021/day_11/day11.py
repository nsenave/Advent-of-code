import unittest
import numpy as np

def line_split(line) :
    return [-999] + list(map(int,list(line))) + [-999]

def parse_input(path) :
    with open(path, 'r') as f :
        res = list(map(line_split, f.read().split('\n')))
        # add border lines to make it simpler
        m = len(res[0])
        res = [[-999]*m] + res + [[-999]*m]
    return np.array(res)

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def adjacent_coords(x,y) :
    res = []
    for dx in (-1,0,1) :
        for dy in (-1,0,1) :
            res.append((x+dx, y+dy))
    res.remove((x,y))
    return res

def r1(arr) :
    a = np.copy(arr)
    n,m = a.shape
    flash_count = 0
    #
    for step in range(100) :
        for i in range(1,n-1) :
            for j in range(1,m-1) :
                a[i,j] += 1
        #
        flashes = np.zeros((n,m))
        for k in range(100) :
            for i in range(1,n-1) :
                for j in range(1,m-1) :
                    if a[i,j] > 9 and not flashes[i,j] :
                        flashes[i,j] = 1
                        flash_count += 1
                        for c in adjacent_coords(i,j) :
                            x,y = c
                            a[x,y] += 1
        #
        for i in range(1,n-1) :
            for j in range(1,m-1) :
                if flashes[i,j] :
                    a[i,j] = 0
    #
    return flash_count



def r2(arr) :
    a = np.copy(arr)
    n,m = a.shape
    flash_count = 0
    omni_flash = False
    step = 0
    #
    while not omni_flash :
        #
        for i in range(1,n-1) :
            for j in range(1,m-1) :
                a[i,j] += 1
        #
        flashes = np.zeros((n,m))
        for k in range(100) :
            for i in range(1,n-1) :
                for j in range(1,m-1) :
                    if a[i,j] > 9 and not flashes[i,j] :
                        flashes[i,j] = 1
                        flash_count += 1
                        for c in adjacent_coords(i,j) :
                            x,y = c
                            a[x,y] += 1
        #
        if sum(sum(flashes)) == 100 :
            omni_flash = True
        #
        for i in range(1,n-1) :
            for j in range(1,m-1) :
                if flashes[i,j] :
                    a[i,j] = 0
        #
        step += 1
    #
    return step



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("-- Part One --")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("-- Part Two --")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
