import unittest
import numpy as np

def line_split(line) :
    return list(map(int, list(line)))

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        puzzle = list(map(line_split, f.read().split('\n')))
    return np.array(puzzle)

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)

a = """19999
19111
11191"""
example_test = np.array(list(map(line_split, a.split('\n'))))



def init(dists, start) :
    n,m = dists.shape
    for i in range(n) :
        for j in range(m) :
            dists[i,j] = np.inf
    dists[start] = 0

def find_min(coords, dists) :
    mini = np.inf
    for c in coords :
        if dists[c] < mini :
            mini = dists[c]
            res = c
    return res

def update_dists(caves, dists, links, c1:tuple, c2:tuple) :
    w12 = caves[c2]
    if dists[c2] > dists[c1] + w12 :
        dists[c2] = dists[c1] + w12
        links[c2] = c1

def list_coords(caves) :
    n,m = caves.shape
    res = []
    for i in range(n) :
        for j in range(m) :
            res.append((i,j))
    return res

def init_links(caves) -> dict :
    return {c:None for c in list_coords(caves)}

def get_neighbours(coord, caves) :
    n,m = caves.shape
    i,j = coord
    res = []
    if i > 0 : res.append((i-1,j))
    if i < n-1 : res.append((i+1,j))
    if j > 0 : res.append((i,j-1))
    if j < m-1 : res.append((i,j+1))
    return res

def dijkstra(caves, start=(0,0)) :
    """Return the shortest path from start to the bottom right corner."""
    n,m = caves.shape
    dists = np.zeros((n,m))
    init(dists, start)
    links = init_links(caves)
    #
    coords = list_coords(caves)
    while coords :
        c1 = find_min(coords, dists)
        coords.remove(c1)
        for c2 in get_neighbours(c1, caves) :
            update_dists(caves, dists, links, c1, c2)
    #
    path = []
    c = (n-1,m-1)
    while c != start :
        path.append(c)
        c = links[c]
    path.append(start)
    return path

def risk_level(caves, path) :
    res = 0
    for c in path[1:] :
        res += caves[c]
    return res

def print_path(caves, path) :
    res = ""
    n,m = caves.shape
    for i in range(n) :
        for j in range(m) :
            if (i,j) in path :
                res += '#'
            else :
                res += str(caves[i,j])
        res += '\n'
    print(res)

def r1(a) :
    path = dijkstra(a)
    print_path(a, path)
    return risk_level(a, path)



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
    print(r1(example_test))
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    # print(f"Puzzle answer:  {r2(puzzle)}")
