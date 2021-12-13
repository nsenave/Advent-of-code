import unittest

import re
import numpy as np

def trace(a) :
    return sum(np.diag(a))

def anti_trace(a) :
    return sum(np.diag(np.flipud(a)))



grid_size = 5

def line_split(line) :
    # pattern = r"([0-9]+\ +){"+ str(grid_size-1) +r"}[0-9]+$" # a bit too much
    return list(map(int, re.split('\ +', re.search("([0-9]+\ +)+[0-9]+$", line).group())))

def grid_split(grid_txt) :
    return np.array(list(map(line_split, grid_txt.split('\n'))))

def import_input(folder:str):
    with open(folder + 'input.txt', 'r') as f :
        draw = list(map(int, f.read().split(',')))
    with open(folder + 'grids.txt', 'r') as f :
        grid = list(map(grid_split, f.read().split('\n\n')))
    return draw, grid

puzzle = import_input('')
example = import_input('example/')

print("Example input:")
print(example[0])
print(example[1])



def turn(n, grid) :
    for i in range(grid_size) :
        for j in range(grid_size) :
            if grid[i,j] == n :
                grid[i,j] = -1
    return grid

def has_won(grid) :
    for i in range(grid_size) :
        if sum(grid[i,:]) == -grid_size :
            return True
        if sum(grid[:,i]) == -grid_size :
            return True
    # (woops diagonals don't count)
    #if trace(grid) == -grid_size :
    #    return True
    #if anti_trace(grid) == -grid_size :
    #    return True
    return False

def sum_unmarked(grid) :
    res = 0
    for i in range(grid_size) :
        for j in range(grid_size) :
            if grid[i,j] != -1 :
                res += grid[i,j]
    return res

def score(grid, last_number) :
    return sum_unmarked(grid) * last_number

def play(d, g) :
    """Return the winning grid and the last number called"""
    for t in range(len(d)) :
        number = d[t]
        for k in range(len(g)) :
            grid = g[k]
            g[k] = turn(number, grid)
            if has_won(grid) :
                return grid, number

def r1(a) :
    d, g = a
    grid, number = play(d, g)
    return score(grid, number)



def play2(d, g) :
    """Return the winning grid and the last number called"""
    grids_number = len(g)
    winning_grids = [0]*grids_number
    for t in range(len(d)) :
        number = d[t]
        for k in range(len(g)) :
            grid = g[k]
            g[k] = turn(number, grid)
            if has_won(grid) :
                winning_grids[k] = 1
            if sum(winning_grids) == grids_number :
                return grid, number

def r2(a) :
    d, g = a
    grid, number = play2(d, g)
    return score(grid, number)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.array = np.array([[1,9],[8,2]])

    def test_traces(self):
        self.assertEqual(trace(self.array), 3)
        self.assertEqual(anti_trace(self.array), 17)
        # check that anti_trace did not modify the array
        self.assertEqual(self.array[0,0], 1)

if __name__ == '__main__':
    unittest.main(exit=False)

    print('--- Part One ---')
    g1, n1 = play(example[0], np.copy(example[1]))
    print(g1, sum_unmarked(g1), n1)
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    g2, n2 = play2(example[0], np.copy(example[1]))
    print(g2, sum_unmarked(g2), n2)
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
