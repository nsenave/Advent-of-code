import os.path
import unittest
import time

import numpy as np

def line_split(line: str) :
    return list(line)

def to_array(raw_map: str) -> np.array:
    return np.array(list(map(line_split, raw_map.split('\n'))), dtype=str)

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return to_array(f.read())



def move_up(cpu, i, j): 
    return (i > 0) and (cpu[i-1,j] != '#')

def move_down(cpu, i, j): 
    return (i < cpu.shape[0] - 1) and (cpu[i+1,j] != '#')

def move_right(cpu, i, j): 
    return (j < cpu.shape[1] - 1) and (cpu[i,j+1] != '#')

def move_left(cpu, i, j): 
    return (j > 0) and (cpu[i,j-1] != '#')

def move(cpu, i, j, i0, j0):
    if move_up(cpu, i, j) and i-1 != i0: return i-1, j
    if move_down(cpu, i, j) and i+1 != i0: return i+1, j
    if move_left(cpu, i, j) and j-1 != j0: return i, j-1
    if move_right(cpu, i, j) and j+1 != j0: return i, j+1
    raise ValueError(f"No possible move at {i, j}")

def moves(cpu, i, j):
    res = []
    if move_up(cpu, i, j): res.append((i-1, j))
    if move_down(cpu, i, j): res.append((i+1, j))
    if move_left(cpu, i, j): res.append((i, j-1))
    if move_right(cpu, i, j): res.append((i, j+1))
    if not res: raise ValueError(f"No possible moves at {i, j}")
    return res

def get_start_position(cpu):
    n, m = cpu.shape
    for i in range(n): 
        for j in range(m):
            if cpu[i, j] == 'S':
                return i, j

def reach_the_end_from(cpu: np.array, i_start, j_start, is_start=True):
    initial_moves = moves(cpu, i_start, j_start)
    assert (is_start and len(initial_moves) == 1) or len(initial_moves) == 2
    for initial_move in initial_moves:
        i0, j0 = i_start, j_start
        i1, j1 = initial_move
        res = 1
        while cpu[i1, j1] != 'E' and cpu[i1, j1] != 'S':
            prev, current = (i1, j1), move(cpu, i1, j1, i0, j0)
            i0, j0 = prev
            i1, j1 = current
            res += 1
        if cpu[i1, j1] == 'E':
            return res
    raise ValueError("Didn't reached the end...")

def compute_distances(cpu):
    res = np.zeros(cpu.shape, dtype=int)
    i0, j0 = get_start_position(cpu)
    res[i0, j0] = reach_the_end_from(cpu, i0, j0)
    i1, j1 = move(cpu, i0, j0, i0, j0)
    while cpu[i1, j1] != 'E':
        res[i1, j1] = reach_the_end_from(cpu, i1, j1, is_start=False)
        prev, current = (i1, j1), move(cpu, i1, j1, i0, j0)
        i0, j0 = prev
        i1, j1 = current
    return res

def reach_the_end_from(cpu: np.array, i_start, j_start, is_start=True):
    initial_moves = moves(cpu, i_start, j_start)
    assert (is_start and len(initial_moves) == 1) or len(initial_moves) == 2
    for initial_move in initial_moves:
        i0, j0 = i_start, j_start
        i1, j1 = initial_move
        res = 1
        while cpu[i1, j1] != 'E' and cpu[i1, j1] != 'S':
            prev, current = (i1, j1), move(cpu, i1, j1, i0, j0)
            i0, j0 = prev
            i1, j1 = current
            res += 1
        if cpu[i1, j1] == 'E':
            return res
    raise ValueError("Didn't reached the end...")

def compute_distances(cpu):
    res = np.zeros(cpu.shape, dtype=int)
    i0, j0 = get_start_position(cpu)
    res[i0, j0] = reach_the_end_from(cpu, i0, j0)
    i1, j1 = move(cpu, i0, j0, i0, j0)
    while cpu[i1, j1] != 'E':
        res[i1, j1] = reach_the_end_from(cpu, i1, j1, is_start=False)
        prev, current = (i1, j1), move(cpu, i1, j1, i0, j0)
        i0, j0 = prev
        i1, j1 = current
    return res

def can_cheat_up(cpu, i, j):
    return (i > 1) and (cpu[i-1,j] == '#') and (cpu[i-2,j] != '#')

def can_cheat_down(cpu, i, j): 
    return (i < cpu.shape[0] - 2) and (cpu[i+1,j] == '#') and (cpu[i+2,j] != '#')

def can_cheat_right(cpu, i, j): 
    return (j < cpu.shape[1] - 2) and (cpu[i,j+1] == '#') and (cpu[i,j+2] != '#')

def can_cheat_left(cpu, i, j): 
    return (j > 1) and (cpu[i,j-1] == '#') and (cpu[i,j-2] != '#')

def local_cheats(cpu, i, j):
    res = []
    if can_cheat_up(cpu, i, j) : res.append((i-2, j))
    if can_cheat_down(cpu, i, j) : res.append((i+2, j))
    if can_cheat_left(cpu, i, j) : res.append((i, j-2))
    if can_cheat_right(cpu, i, j) : res.append((i, j+2))
    return res

def cheat_values(cpu, i, j, distances, min_save):
    res = []
    for cheat_coords in local_cheats(cpu, i, j):
        res.append(distances[i,j] - distances[cheat_coords[0], cheat_coords[1]] - 2)
    return list(filter(lambda value: value >= min_save, res))

def find_cheats(cpu, distances, min_save=0, debug=False):
    res = []
    i0, j0 = get_start_position(cpu)
    start_distance = distances[i0, j0]
    res.extend(cheat_values(cpu, i0, j0, distances, min_save))
    i1, j1 = move(cpu, i0, j0, i0, j0)
    res = []
    while cpu[i1, j1] != 'E':
        res.extend(cheat_values(cpu, i1, j1, distances, min_save))
        prev, current = (i1, j1), move(cpu, i1, j1, i0, j0)
        i0, j0 = prev
        i1, j1 = current
        distance = distances[i1, j1]
        if (not debug) and distance % 1000 == 0:
            print(f"On the way: {start_distance - distance}/{start_distance}...")
    return res

def print_cheats(cheats):
    counts = {}
    for value in cheats:
        if value not in counts:
            counts[value] = 0
        counts[value] += 1
    for value in counts.keys():
        count = counts[value]
        if count == 1:
            print(f"There is one cheat that saves {value} picoseconds.")
            continue
        print(f"There are {count} cheats that save {value} picoseconds.")

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    cpu = puzzle_input
    distances = compute_distances(cpu)
    i, j = get_start_position(cpu)
    print("Distances computed")
    print(f"Distance at start: {distances[i, j]}")
    min_save = 0 if debug else 100
    cheats = find_cheats(cpu, distances, min_save, debug)
    if debug:
        print(distances)
        print(cpu[7,5])
        print(local_cheats(cpu, 7, 7))
        print(cheat_values(cpu, 7, 7, distances, 0))
        print_cheats(cheats)
    return len(cheats)



def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for x in puzzle_input :
        pass
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')

    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}") # 1387, 1388 too low
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
