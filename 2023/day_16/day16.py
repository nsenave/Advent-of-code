import os.path
import unittest
from enum import Enum
import numpy as np
import sys

class Contraption:
    def __init__(self, layout: list) -> None:
        self.layout = layout
        self.shape = len(layout), len(layout[0])
    def __str__(self) -> str:
        return '\n'.join(self.layout)
    def __getitem__(self, position: tuple) -> str:
        i, j = position
        return self.layout[i][j]

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return Contraption(f.read().split('\n'))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)

example_enegized = """######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#.."""



Direction = Enum('Direction', ['UP', 'DOWN', 'RIGHT', 'LEFT'])

def beam_move(contraption: Contraption, energy: np.array, position: tuple, direction: Direction, memo: dict) -> None:
    i, j = position
    if position in memo[direction]:
        return None
    memo[direction].append(position)
    if direction is Direction.UP:
        move_up(contraption, energy, i, j, memo)
    elif direction is Direction.DOWN:
        move_down(contraption, energy, i, j, memo)
    elif direction is Direction.LEFT:
        move_left(contraption, energy, i, j, memo)
    elif direction is Direction.RIGHT:
        move_right(contraption, energy, i, j, memo)

def move_up(contraption, energy, i, j, memo) -> None:
    if i == 0:
        return None
    next_position = (i-1, j)
    energy[next_position] += 1
    tile = contraption[next_position]
    if tile == '-':
        beam_move(contraption, energy, next_position, Direction.LEFT, memo)
        beam_move(contraption, energy, next_position, Direction.RIGHT, memo)
    elif tile == '/':
        beam_move(contraption, energy, next_position, Direction.RIGHT, memo)
    elif tile == '\\':
        beam_move(contraption, energy, next_position, Direction.LEFT, memo)
    else:
        beam_move(contraption, energy, next_position, Direction.UP, memo)
    return None

def move_down(contraption, energy, i, j, memo) -> None:
    if i+1 == contraption.shape[0]:
        return None
    next_position = (i+1, j)
    energy[next_position] += 1
    tile = contraption[next_position]
    if tile == '-':
        beam_move(contraption, energy, next_position, Direction.LEFT, memo)
        beam_move(contraption, energy, next_position, Direction.RIGHT, memo)
    elif tile == '/':
        beam_move(contraption, energy, next_position, Direction.LEFT, memo)
    elif tile == '\\':
        beam_move(contraption, energy, next_position, Direction.RIGHT, memo)
    else:
        beam_move(contraption, energy, next_position, Direction.DOWN, memo)
    return None

def move_left(contraption, energy, i, j, memo) -> None:
    if j == 0:
        return None
    next_position = (i, j-1)
    energy[next_position] += 1
    tile = contraption[next_position]
    if tile == '|':
        beam_move(contraption, energy, next_position, Direction.UP, memo)
        beam_move(contraption, energy, next_position, Direction.DOWN, memo)
    elif tile == '/':
        beam_move(contraption, energy, next_position, Direction.DOWN, memo)
    elif tile == '\\':
        beam_move(contraption, energy, next_position, Direction.UP, memo)
    else:
        beam_move(contraption, energy, next_position, Direction.LEFT, memo)
    return None

def move_right(contraption, energy, i, j, memo) -> None:
    if j+1 == contraption.shape[1]:
        return None
    next_position = (i, j+1)
    energy[next_position] += 1
    tile = contraption[next_position]
    if tile == '|':
        beam_move(contraption, energy, next_position, Direction.UP, memo)
        beam_move(contraption, energy, next_position, Direction.DOWN, memo)
    elif tile == '/':
        beam_move(contraption, energy, next_position, Direction.UP, memo)
    elif tile == '\\':
        beam_move(contraption, energy, next_position, Direction.DOWN, memo)
    else:
        beam_move(contraption, energy, next_position, Direction.RIGHT, memo)
    return None

def count_energized_tiles(energy: np.array) -> int:
    n, m = energy.shape
    res = 0
    for i in range(n):
        for j in range(m):
            if energy[i, j] >= 1:
                res += 1
    return res

def energy_score(contraption: Contraption, start_position: tuple, start_direction: Direction) -> int:
    energy = np.zeros(contraption.shape, dtype=int)
    memo = {
        Direction.UP: [],
        Direction.DOWN: [],
        Direction.LEFT: [],
        Direction.RIGHT: []
    }
    beam_move(contraption, energy, start_position, start_direction, memo)
    #print(energy)
    return count_energized_tiles(energy)

def r1(a) :
    if a is None :
        return None
    return energy_score(a, (0, -1), Direction.RIGHT)



def r2(a) :
    if a is None :
        return None
    result = 0
    contraption = a
    n, m = contraption.shape
    for i in range(n):
        result = max(result, energy_score(contraption, (i, -1), Direction.RIGHT))
    print('Beam from left configrations tested')
    for i in range(n):
        result = max(result, energy_score(contraption, (i, n), Direction.LEFT))
    print('Beam from right configrations tested')
    for j in range(m):
        result = max(result, energy_score(contraption, (-1, j), Direction.DOWN))
    print('Beam from up configrations tested')
    for j in range(m):
        result = max(result, energy_score(contraption, (m, j), Direction.UP))
    print('Beam from down configrations tested')
    return result



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)

    sys.setrecursionlimit(10000)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
