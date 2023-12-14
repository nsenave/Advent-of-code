import os.path
import unittest
import numpy as np
import sys

class PipeMaze:

    def __init__(self) -> None:
        self.rows = []
        self.x_size = 0
        self.y_size = None
        self.start_coords = None

    def __str__(self) -> str:
        return '\n'.join(self.rows)
    
    def add_row(self, row:str):
        m = len(row)
        if self.y_size is None:
            self.y_size = m
        if m != self.y_size:
            return ValueError("Inconsistent row length.")
        self.rows.append(row)
        self.x_size += 1

    def get(self, i, j) -> str:
        return self.rows[i][j]
    
    def get_tile(self, coords) -> str:
        i,j = coords
        return self.get(i,j)
    
    def get_start_coords(self) -> tuple:
        if self.start_coords is not None:
            return self.start_coords
        for i in range(self.x_size):
            for j in range(self.y_size):
                if self.get(i,j) == 'S':
                    self.start_coords = (i,j)
                    return (i,j)
        raise ValueError("Didn't find any starting point.")



def parse_content(raw_input: str) :
    """Parse input into a PipeMaze object and add extra '.' around to avoid out of range errors."""
    pipe_maze = PipeMaze()
    input_lines = raw_input.split('\n')
    m = len(input_lines[0])
    pipe_maze.add_row(''.join(['.' for _ in range(m+2)]))
    for row in input_lines:
        pipe_maze.add_row('.' + row + '.')
    pipe_maze.add_row(''.join(['.' for _ in range(m+2)]))
    return pipe_maze

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return parse_content(f.read())

puzzle = parse_input('input.txt')

example1 = parse_content(""".....
.S-7.
.|.|.
.L-J.
.....""")

example2 = parse_content("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF""")

example3 = parse_content("""..F7.
.FJ|.
SJ.L7
|F--J
LJ...""")

example4 = parse_content("""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""")

print("Example 1:")
print(example1)



# Tile kinds: | - L J 7 F . S

def compute_distances_from_start(pipe_maze: PipeMaze) -> np.array:
    distances = np.zeros((pipe_maze.x_size, pipe_maze.y_size), dtype=int)
    start_coords = pipe_maze.get_start_coords()
    propagate(pipe_maze, distances, start_coords, start_coords)
    return distances

def propagate(pipe_maze, distances, current_coords, previous_coords):
    i,j = current_coords
    north_coords = (i-1, j)
    south_coords = (i+1, j)
    east_coords = (i, j+1)
    west_coords = (i, j-1)
    current_dist = distances[i,j]
    if can_propagate(north_coords, previous_coords, pipe_maze, ('|', '7', 'F')):
        if update_neighbour_distance(distances, current_dist, north_coords):
            propagate(pipe_maze, distances, north_coords, current_coords)
    if can_propagate(south_coords, previous_coords, pipe_maze, ('|', 'L', 'J')):
        if update_neighbour_distance(distances, current_dist, south_coords):
            propagate(pipe_maze, distances, south_coords, current_coords)
    if can_propagate(east_coords, previous_coords, pipe_maze, ('-', 'J', '7')):
        if update_neighbour_distance(distances, current_dist, east_coords):
            propagate(pipe_maze, distances, east_coords, current_coords)
    if can_propagate(west_coords, previous_coords, pipe_maze, ('-', 'L', 'F')):
        if update_neighbour_distance(distances, current_dist, west_coords):
            propagate(pipe_maze, distances, west_coords, current_coords)

def can_propagate(next_coords, previous_coords, pipe_maze, accepted_tiles):
    return next_coords != previous_coords and pipe_maze.get_tile(next_coords) in accepted_tiles

def update_neighbour_distance(distances, current_dist, neighbour_coords):
    neighbour_distance = distances[neighbour_coords]
    if neighbour_distance == 0:
        distances[neighbour_coords] = current_dist + 1
        return True
    else:
        if current_dist + 1 > neighbour_distance:
            return False
        distances[neighbour_coords] = current_dist + 1
        return True

def r1(a) :
    if a is None :
        return None
    distances = compute_distances_from_start(a)
    #print(distances)
    return distances.max()




example2_1 = parse_input('input-part-two-example-1.txt')
example2_2 = parse_input('input-part-two-example-2.txt')
example2_3 = parse_input('input-part-two-example-3.txt')

def compute_pipe_shape(pipe_maze: PipeMaze) -> np.array:
    pipe_shape = np.zeros((pipe_maze.x_size, pipe_maze.y_size), dtype=int)
    start_coords = pipe_maze.get_start_coords()
    pipe_shape[start_coords] = 1
    propagate2(pipe_maze, pipe_shape, start_coords, start_coords)
    return pipe_shape

def propagate2(pipe_maze, pipe_shape, current_coords, previous_coords):
    i,j = current_coords
    north_coords = (i-1, j)
    south_coords = (i+1, j)
    east_coords = (i, j+1)
    west_coords = (i, j-1)
    if can_propagate2(north_coords, previous_coords, pipe_maze, ('|', '7', 'F'), pipe_shape):
        pipe_shape[north_coords] = 1
        propagate2(pipe_maze, pipe_shape, north_coords, current_coords)
    if can_propagate2(south_coords, previous_coords, pipe_maze, ('|', 'L', 'J'), pipe_shape):
        pipe_shape[south_coords] = 1
        propagate2(pipe_maze, pipe_shape, south_coords, current_coords)
    if can_propagate2(east_coords, previous_coords, pipe_maze, ('-', 'J', '7'), pipe_shape):
        pipe_shape[east_coords] = 1
        propagate2(pipe_maze, pipe_shape, east_coords, current_coords)
    if can_propagate2(west_coords, previous_coords, pipe_maze, ('-', 'L', 'F'), pipe_shape):
        pipe_shape[west_coords] = 1
        propagate2(pipe_maze, pipe_shape, west_coords, current_coords)

def can_propagate2(next_coords, previous_coords, pipe_maze, accepted_tiles, pipe_shape):
    return next_coords != previous_coords and pipe_maze.get_tile(next_coords) in accepted_tiles and pipe_shape[next_coords] == 0

def fill_pipe(pipe_shape: np.array, is_example=False) -> int:
    result = 0
    n, m = pipe_shape.shape
    for i in range(1, n-1):
        is_inside = False
        j = 1
        while j < m-1:
            if pipe_shape[i,j] > 0:
                is_inside = not is_inside
                while j < m and pipe_shape[i,j] > 0:
                    j += 1
                is_inside = pipe_shape[i-1, j] > 0
            else:
                if is_inside:
                    pipe_shape[i,j] = 2 # just for visualization
                    result += 1
                j += 1
    if is_example: print(pipe_shape)
    return result

def r2(a) :
    if a is None :
        return None
    # using the distances matrix would have worked fine too
    pipe_shape = compute_pipe_shape(a)
    #print(pipe_shape)
    return fill_pipe(pipe_shape)



u_shape = """
.........
.###.###.
.#.#.#.#.
.#.###.#.
.#.....#.
.#######.
.........
"""

u_array = np.array(list(map(lambda line: [0 if c == '.' else 1 for c in line], u_shape.split('\n')[1:-1])))

print("U array:")
print(u_array)

class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(9, fill_pipe(u_array))
        self.assertEqual(4, r2(example2_1))
        self.assertEqual(8, r2(example2_2))
        self.assertEqual(10, r2(example2_3))

if __name__ == '__main__':
    unittest.main(exit=False)

    sys.setrecursionlimit(100000)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example1)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example2_1, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
