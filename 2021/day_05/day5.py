import unittest
import numpy as np

def line_split(line) :
    return list(map(lambda c: tuple(map(int, (c.split(',')))), line.split(' -> ')))

with open('input.txt', 'r') as f :
    puzzle = list(map(line_split, f.read().split('\n')))

with open('example/input.txt', 'r') as f :
    example = list(map(line_split, f.read().split('\n')))

print("Example input:")
print(example)



def get_size(lines) :
    res = 0
    for line in lines :
        for c in line :
            m = max(c)
            if m > res :
                res = m
    return res + 1

def lines_map(lines) :
    size = get_size(lines)
    res = np.zeros((size, size))
    for line in lines :
        start, end = line
        x1, y1 = start
        x2, y2 = end
        if x1==x2 or y1==y2 :
            x, xf = min(x1,x2), max(x1,x2)
            y, yf = min(y1,y2), max(y1,y2)
            if x != xf :
                while x <= xf :
                    res[x,y] += 1
                    x += 1
            else :
                while y <= yf :
                    res[x,y] += 1
                    y += 1
    return res

def count_in_map(a) :
    res = 0
    size = len(a)
    for x in range(size) :
        for y in range(size) :
            if a[x,y] > 1 :
                res += 1
    return res

def r1(a) :
    return count_in_map(lines_map(a))



def lines_map2(lines) :
    size = get_size(lines)
    res = np.zeros((size, size))
    for line in lines :
        start, end = line
        x1, y1 = start
        x2, y2 = end
        if x1==x2 or y1==y2 :
            x, xf = min(x1,x2), max(x1,x2)
            y, yf = min(y1,y2), max(y1,y2)
            if x != xf :
                while x <= xf :
                    res[x,y] += 1
                    x += 1
            else :
                while y <= yf :
                    res[x,y] += 1
                    y += 1
        else :
            x,y = x1,y1
            x_up = x1 <= x2
            y_up = y1 <= y2
            while x != x2 :
                res[x,y] += 1
                if x_up :
                    x += 1
                else :
                    x -= 1
                if y_up :
                    y += 1
                else :
                    y -= 1
            res[x2, y2] += 1
    return res

def r2(a) :
    return count_in_map(lines_map2(a))



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(get_size(example))
    print(lines_map(example).transpose())
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(lines_map2(example).transpose())
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
