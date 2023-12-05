import os.path
import unittest
from typing import List, Tuple
import time

def section_split(section: str) :
    res = []
    for map_instruction in section.split('\n')[1:]:
        res.append(list(map(int, map_instruction.split())))
    return res

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        sections = f.read().split('\n\n')
        seeds = list(map(int, sections[0].split(': ')[1].split()))
        almanac = list(map(section_split, sections[1:]))
        return seeds, almanac

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def r1(a, is_example=False) :
    if a is None :
        return None
    seeds, almanac = a
    locations = []
    for seed in seeds:
        start = seed
        for section in almanac:
            start = to_destination(start, section)
        locations.append(start)
    if is_example:
        print(locations)
    return min(locations)

def to_destination(start: int, section) -> int:
    for map_instruction in section:
        source = map_instruction[1]
        destination = map_instruction[0]
        range_value = map_instruction[2]
        if start in range(source, source+range_value):
            return destination + (start - source)
    return start



def to_source(some_destination: int, section) -> int:
    for map_instruction in section:
        source = map_instruction[1]
        destination = map_instruction[0]
        range_value = map_instruction[2]
        if some_destination in range(destination, destination+range_value):
            return some_destination - destination + source
    return some_destination

def construct_pairs(seeds: list) -> List[Tuple]:
    res = []
    for k in range(0, len(seeds), 2):
        seed = seeds[k]
        seed_range = seeds[k+1]
        res.append((seed, seed_range))
    return res

def is_in_seeds(seed: int, seed_pairs) -> bool:
    for seed_pair in seed_pairs:
        start_seed, seed_range = seed_pair
        if seed in range(start_seed, start_seed+seed_range):
            return True
    return False

def r2(a) :
    if a is None :
        return None
    seeds, almanac = a
    seed_pairs = construct_pairs(seeds)
    location = 0
    seed_found = False
    while not seed_found:
        number = location
        for section in reversed(almanac):
            number = to_source(number, section)
        seed = number
        if is_in_seeds(seed, seed_pairs):
            seed_found = True
        else:
            location += 1
    return location



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")

    t0 = time.time()
    answer2 = r2(puzzle)
    t1 = time.time()

    print(f"Puzzle answer:  {answer2}")
    print(f"Time to compute part two: {(t1-t0)//60} minutes and {(t1-t0)%60} seconds")
