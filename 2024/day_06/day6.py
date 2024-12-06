import os.path
import unittest
import time

import numpy as np

def line_split(line: str) :
    return list(line)

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

def show_maze(maze) -> str:
    """Works for both python list or numpy array."""
    print('\n'.join(map(lambda line: ''.join(line), maze)) + '\n')

print("Example input:")
print(example)
show_maze(example)



def get_starting_position(maze) -> tuple:
    for i in range(len(maze)) :
        for j in range(len(maze[0])) :
            if maze[i,j] == '^' :
                return i,j
    raise ValueError("No starting position in given maze.")

def rotate_maze(maze, i, j) :
    i, j = maze.shape[1] - 1 - j, i
    return (np.rot90(maze), i, j)

def move_forward(maze, i, j) :
    while maze[i,j] != '#':
        maze[i,j] = 'X'
        i -= 1
        if i == 0 and maze[i,j] != '#' :
            maze[i,j] = 'X'
            return -1
    return i+1

def count_positions(maze) :
    res = 0
    for i in range(len(maze)) :
        for j in range(len(maze[0])) :
            if maze[i,j] == 'X' :
                res += 1
    return res

def guard_patrol(puzzle_input, debug, max_steps=1000):
    maze = np.array(puzzle_input, dtype=str)
    i,j = get_starting_position(maze)
    rotate_clock = 0
    steps = 0
    while steps < max_steps :
        if debug:
            print("Before moving:")
            show_maze(maze)
        i = move_forward(maze, i, j)
        if i == -1 :
            break
        if debug:
            print("After moving:")
            show_maze(maze)
        maze, i, j = rotate_maze(maze, i, j)
        rotate_clock += 1
        rotate_clock %= 4
        steps += 1
    return maze, steps, rotate_clock

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    maze, steps, rotate_clock = guard_patrol(puzzle_input, False)
    if debug:
        # Put the maze in its original orientation
        while rotate_clock != 0:
            maze = np.rot90(maze)
            rotate_clock += 1
            rotate_clock %= 4
        print(f"Final map:")
        show_maze(maze)
    print(f"Number of steps: {steps}")
    return count_positions(maze)



def print_progession(i, j, row_count, col_count) :
    print(f"Progression: {round((i + (j / col_count)) / row_count * 100, 1)} %")

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    max_steps = 1000
    res = 0
    row_count = len(puzzle_input)
    col_count = len(puzzle_input[0])
    for i in range(row_count) :
        for j in range(col_count) :
            if puzzle_input[i][j] == '.' :
                puzzle_input[i][j] = '#'
                steps = guard_patrol(puzzle_input, False, max_steps)[1]
                if steps == max_steps:
                    res += 1
                puzzle_input[i][j] = '.'
            if (not debug) and (j == col_count//3 or j == col_count//3*2):
                print_progession(i, j+1, row_count, col_count)
        print_progession(i+1, 0, row_count, col_count)
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(get_starting_position(np.array(example,dtype=str)), (6,4))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")
    
    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
