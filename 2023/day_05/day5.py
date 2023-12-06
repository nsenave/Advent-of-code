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



# Part 2 brute force method, but start from location and find if there is a corresponding seed
# for location=0,1,2,3,... untill a seed is found.

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



# Part 2 by resolving the seed ranges against the different steps of the almanac
# Idea:
#       [-------------------]     (range of seeds)
# <------------>      <---------> (maps of a section of the almanac)
#       [******][----][*****]     (ranges of seeds after this section)
# (those with ** are then shifted)

class StepInterval :
    def __init__(self, start: int, end: int, shift: int):
        if end < start:
            raise ValueError(f"end ({end}) < start ({start})")
        self.start = start
        self.end = end
        self.shift = shift
    def __str__(self):
        return f"[{self.start}, {self.end}], shift={self.shift}"
    def __repr__(self):
        return str(self)

class SeedInterval(StepInterval) :
    def __init__(self, start: int, end: int):
        super().__init__(start, end, 0)
    def __str__(self):
        return f"Seeds [{self.start}, {self.end}]"

def r2_bis(a):
    seeds, almanac = a
    # Re-arange seeds input
    seed_intervals = []
    for k in range(0, len(seeds), 2):
        start_seed = seeds[k]
        seed_range = seeds[k+1]
        seed_intervals.append(SeedInterval(start_seed, start_seed+seed_range))
    #print(seed_intervals)
    # Re-arange almanac input
    steps = []
    for section in almanac:
        step = []
        for map_instruction in section:
            source = map_instruction[1]
            destination = map_instruction[0]
            range_value = map_instruction[2]
            step.append(StepInterval(source, source+range_value, destination-source))
            step.sort(key=lambda interval: interval.start, reverse=True)
        steps.append(step)
    #print(steps)
    # Resolve seed intervals against steps
    for step in steps:
        new_intervals = []
        while seed_intervals:
            seed_interval = seed_intervals.pop()
            new_intervals += apply_step(seed_interval, step)
        seed_intervals = new_intervals
    #print(seed_intervals)
    # Find the minimum location by only computing edges of each seed interval
    min_location = 99999999
    for seed_interval in seed_intervals:
        for number in (seed_interval.start, seed_interval.end - 1):
            for section in almanac:
                number = to_destination(number, section)
            location = number
            if location < min_location:
                min_location = location
    return min_location

def no_overlap(interval1: StepInterval, interval2: StepInterval) -> bool:
    """Return true if there is not overlap between the two intervals."""
    return (interval1.start > interval2.end) or (interval1.end < interval2.start)

def is_inside(interval1: StepInterval, interval2: StepInterval) -> bool:
    """Return true if the first interval is inside the second."""
    return (interval1.start >= interval2.start) and (interval1.end <= interval2.end)

def is_larger_below(interval1: StepInterval, interval2: StepInterval) -> bool:
    """Return true if the first interval starts before the second."""
    return interval1.start < interval2.start

def is_larger_above(interval1: StepInterval, interval2: StepInterval) -> bool:
    """Return true if the first interval ends afetr the second."""
    return interval1.end > interval2.end

def is_larger_both_sides(interval1: StepInterval, interval2: StepInterval) -> bool:
    """Return true if the first interval is larger than the second from both sides."""
    return is_larger_below(interval1, interval2) and is_larger_above(interval1, interval2)

def shifted_interval(seed_interval: SeedInterval, shift: int) -> SeedInterval:
    """Returns a new seed interval object, its start and end beeing shifted by the step interval."""
    return SeedInterval(seed_interval.start + shift, seed_interval.end + shift)

def apply_step(seed_interval: SeedInterval, step: List[StepInterval]) -> List[SeedInterval]:
    for step_interval in step:
        shift = step_interval.shift
        if no_overlap(seed_interval, step_interval):
            continue
        if is_inside(seed_interval, step_interval):
            return [shifted_interval(seed_interval, shift)]
        if is_larger_both_sides(seed_interval, step_interval):
            return apply_step(SeedInterval(seed_interval.start, step_interval.start - 1), step) + [shifted_interval(SeedInterval(step_interval.start, step_interval.end), shift)] + apply_step(SeedInterval(step_interval.end + 1, seed_interval.end), step)
        if is_larger_below(seed_interval, step_interval):
            return apply_step(SeedInterval(seed_interval.start, step_interval.start - 1), step) + [shifted_interval(SeedInterval(step_interval.start, seed_interval.end), shift)]
        if is_larger_above(seed_interval, step_interval):
            return [shifted_interval(SeedInterval(seed_interval.start, step_interval.end), shift)] + apply_step(SeedInterval(step_interval.end + 1, seed_interval.end), step)
        raise RuntimeError("Didn't expect this")
    # If none overlap was found, simply return an identical interval
    return [SeedInterval(seed_interval.start, seed_interval.end)]




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

    # t0 = time.time()
    # answer2 = r2(puzzle)
    # t1 = time.time()

    # print(f"Puzzle answer:  {answer2}")
    # print(f"Time to compute part two: {(t1-t0)//60} minutes and {(t1-t0)%60} seconds")

    print(f"Example result (method 2): {r2_bis(example)}")

    t0 = time.time()
    answer2 = r2_bis(puzzle)
    t1 = time.time()

    print(f"Puzzle answer:  {answer2}")
    print(f"Time to compute part two: {t1-t0} seconds")

    print(f"Puzzle result (method 2):  {answer2}")
