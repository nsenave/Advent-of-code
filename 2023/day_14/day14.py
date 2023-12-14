import os.path
import unittest
from enum import Enum
from copy import deepcopy

def line_split(line: str) :
    res = list(line)
    return res

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

def platform_to_string(platform: list) -> str:
    return '\n'.join(list(map(lambda line: ''.join(line), platform)))

def print_platform(platform: list) -> None:
    if len(platform) > 10:
        print("Platform is too large to be displayed")
        return None
    print(platform_to_string(platform))

print("Example input:")
print_platform(example)



Direction = Enum('Direction', ['NORTH', 'WEST', 'SOUTH', 'EAST'])

def is_north_or_west(direction: Direction) -> bool:
    return direction is Direction.NORTH or direction is Direction.WEST

def is_south_or_east(direction: Direction) -> bool:
    return direction is Direction.SOUTH or direction is Direction.EAST

def shift_north_or_west(platform: list, direction: Direction) -> list:
    if not is_north_or_west(direction):
        raise ValueError(f"Wrong direction: {direction}. North or west expected")
    if direction is Direction.NORTH:
        shift_rock_function = shift_rock_north
    if direction is Direction.WEST:
        shift_rock_function = shift_rock_west
    n, m = len(platform), len(platform[0])
    for i in range(n):
        for j in range(m):
            if platform[i][j] == 'O':
                shift_rock_function(platform, i, j)
    return platform

def shift_south_or_east(platform: list, direction: Direction) -> list:
    if not is_south_or_east(direction):
        raise ValueError(f"Wrong direction: {direction}. South or east expected")
    if direction is Direction.SOUTH:
        shift_rock_function = shift_rock_south
    if direction is Direction.EAST:
        shift_rock_function = shift_rock_east
    n, m = len(platform), len(platform[0])
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if platform[i][j] == 'O':
                shift_rock_function(platform, i, j)
    return platform

def shift_rock_north(platform: list, i_rock: int, j_rock: int) -> list:
    i = i_rock
    while i-1 >= 0 and platform[i-1][j_rock] == '.' :
        i -= 1
    if i != i_rock:
        platform[i_rock][j_rock] = '.'
        platform[i][j_rock] = 'O'
    return platform

def shift_rock_west(platform: list, i_rock: int, j_rock: int) -> list:
    j = j_rock
    while j-1 >= 0 and platform[i_rock][j-1] == '.' :
        j -= 1
    if j != j_rock:
        platform[i_rock][j_rock] = '.'
        platform[i_rock][j] = 'O'
    return platform

def shift_rock_south(platform: list, i_rock: int, j_rock: int) -> list:
    n = len(platform)
    i = i_rock
    while i+1 < n and platform[i+1][j_rock] == '.' :
        i += 1
    if i != i_rock:
        platform[i_rock][j_rock] = '.'
        platform[i][j_rock] = 'O'
    return platform

def shift_rock_east(platform: list, i_rock: int, j_rock: int) -> list:
    m = len(platform[0])
    j = j_rock
    while j+1 < m and platform[i_rock][j+1] == '.' :
        j += 1
    if j != j_rock:
        platform[i_rock][j_rock] = '.'
        platform[i_rock][j] = 'O'
    return platform

def apply_cycle(platform: list) -> list:
    shift_north_or_west(platform, Direction.NORTH)
    shift_north_or_west(platform, Direction.WEST)
    shift_south_or_east(platform, Direction.SOUTH)
    shift_south_or_east(platform, Direction.EAST)
    return platform

def compute_north_load(platform: list) -> int:
    res = 0
    n = len(platform)
    for i in range(n):
        res += platform[i].count('O') * (n-i)
    return res

def r1(a) :
    if a is None :
        return None
    platform = deepcopy(a)
    return compute_north_load(shift_north_or_west(platform, Direction.NORTH))



def apply_n_cycles(platform: list, n=1) -> list:
    for _ in range(n):
        apply_cycle(platform)
    return platform

def r2(a) :
    if a is None :
        return None
    platform = deepcopy(a)
    # apply_cycle(platform)
    # print("After 1 cycle:")
    # print_platform(platform)
    # apply_cycle(platform)
    # print("After 2 cycles:")
    # print_platform(platform)
    # apply_cycle(platform)
    # print("After 3 cycles:")
    # print_platform(platform)
    # "If you feel like printing something, write a test instead (see TestsOfToday)"
    sequence_start, sequence_length = look_for_sequence(platform)
    if not check_sequence(deepcopy(a), sequence_start, sequence_length):
        print("Hash function has fooled us!!")
    else:
        print("Sequence found is correct :)")
    apply_n_cycles(platform, (1000000000-sequence_start)%sequence_length)
    return compute_north_load(platform)

def hash_platform(platform: list) -> int:
    return hash(platform_to_string(platform))

def look_for_sequence(platform, max_iteration=1000):
    hashes = []
    current_hash = hash_platform(platform)
    step = 0
    while step <= max_iteration:
        if current_hash in hashes:
            sequence_start = hashes.index(current_hash)
            sequence_length = step - sequence_start
            print(f"Cycles start repeating after the {sequence_start}-th cycle. Repeating sequence of length {sequence_length}.")
            return sequence_start, sequence_length
        hashes.append(current_hash)
        apply_cycle(platform)
        current_hash = hash_platform(platform)
        step += 1
    print("Didn't find a repeating sequence :(")

def check_sequence(platform: list, sequence_start: int, sequence_length: int) -> bool:
    platform1 = deepcopy(apply_n_cycles(platform, n=sequence_start))
    platform2 = deepcopy(apply_n_cycles(platform, n=sequence_length))
    return compare_platforms(platform1, platform2)

def compare_platforms(platform1: list, platform2: list) -> bool:
    n, m = len(platform1), len(platform1[0])
    if len(platform2) != n:
        return False
    if len(platform2[0]) != m:
        return False
    for i in range(n):
        for j in range(m):
            if platform1[i][j] != platform2[i][j]:
                return False
    return True



example_after_1_cycle = """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""

example_after_2_cycles = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""

example_after_3_cycles = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""

class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_shift(self):
        self.assertEqual([['O'], ['.'], ['.']], shift_rock_north([['.'], ['.'], ['O']], 2, 0))
    
    def test_cycles(self):
        self.assertEqual(example_after_1_cycle, platform_to_string(apply_n_cycles(deepcopy(example), n=1)))
        self.assertEqual(example_after_2_cycles, platform_to_string(apply_n_cycles(deepcopy(example), n=2)))
        self.assertEqual(example_after_3_cycles, platform_to_string(apply_n_cycles(deepcopy(example), n=3)))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
