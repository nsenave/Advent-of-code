import os.path
import unittest
import time

def parse_stones(raw_stones: str) -> list:
    return list(map(int, raw_stones.split(' ')))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return parse_stones(f.read())



def rules(stone: int) -> int:
    if stone == 0:
        return [1]
    engraved = str(stone)
    length = len(engraved)
    half = length // 2
    if length % 2 == 0:
        return [int(engraved[:half]), int(engraved[half:])]
    return [stone * 2024]

def blink(stones: list) -> list:
    counter = 0
    new_stones = []
    for stone in stones:
        new_stones.extend(rules(stone))
    counter += 1
    return new_stones

def n_blinks(stones: list, n: int, debug=False) -> list:
    for k in range(1, n+1):
        stones = blink(stones)
        if debug and k <= 6:
            s = "s" if k > 1 else ""
            print(f"After {k} blink{s}:") # beautiful
            print(stones)
            print("")
        if debug and k == 6:
            print(f"Current stones count: {len(stones)}")
    return stones

def count_after_n_blinks(stones, n):
    return len(n_blinks(stones, n))

def r1(puzzle_input, n) :
    if puzzle_input is None:
        return None
    res = 0
    for stone in puzzle_input:
        res += count_after_n_blinks([stone], n)
    return res



def add_stone(stone, count, counts):
    if stone not in counts:
        counts[stone] = count
        return
    counts[stone] += count

def cache_blink(stone, cache):
    if stone in cache:
        return cache[stone]
    blinked = blink([stone])
    cache[stone] = blinked
    return blinked

def blink2(counts: dict, cache):
    new_counts = {}
    for stone in counts.keys():
        new_stones = cache_blink(stone, cache)
        for new_stone in new_stones:
            add_stone(new_stone, counts[stone], new_counts)
    return new_counts

def r2(puzzle_input, n, debug=False) :
    if puzzle_input is None:
        return None
    counts = {}
    cache = {}
    for stone in puzzle_input:
        add_stone(stone, 1, counts)
    for _ in range(n):
        counts = blink2(counts, cache)
    if debug:
        print(counts)
    return sum(counts.values())



"""
Initial arrangement:
125 17

After 1 blink:
253000 1 7

After 2 blinks:
253 0 2024 14168

After 3 blinks:
512072 1 20 24 28676032

After 4 blinks:
512 72 2024 2 0 2 4 2867 6032

After 5 blinks:
1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

After 6 blinks:
2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2
"""

class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        stones = parse_stones("0 1 10 99 999")
        expected = parse_stones("1 2024 1 0 9 9 2021976")
        self.assertEqual(expected, blink(stones))
    """
    def test_2024(self):
        print("")
        stones = [2024]
        for n in range(6):
            stones = blink(stones)
            print(f"2024 after {n+1} blinks: {stones}")
    
    def test_single_digits(self):
        for number in range(1, 10):
            print("")
            stones = [number]
            for n in range(6):
                stones = blink(stones)
                print(f"{number} after {n+1} blinks: {stones}")
    """

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')

    print("--- Part One ---")
    t0 = time.time()
    n_blinks(example, 6, debug=True) # just for printing
    print(f"Example result: {r1(example, 25)}")
    print(f"Puzzle answer:  {r1(puzzle, 25)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result after 25: {r2(example, 25)}")
    print(f"Puzzle answer after 25:  {r2(puzzle, 25)}")
    print(f"Example result: {r2(example, 75)}")
    print(f"Puzzle answer:  {r2(puzzle, 75)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
