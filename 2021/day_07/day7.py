import unittest
from statistics import median

with open('input.txt', 'r') as f :
    puzzle = list(map(int, f.read().split(',')))

with open('example/input.txt', 'r') as f :
    example = list(map(int, f.read().split(',')))

print("Example input:")
print(example)



def try_position(n, positions) :
    fuel = 0
    for p in positions :
        fuel += abs(n-p)
    return fuel

def try_position2(n, positions) :
    fuel = 0
    for p in positions :
        diff = abs(n-p)
        fuel += diff*(diff+1)//2
    return fuel

def brut_force(positions, try_function) :
    min_fuel = try_function(0, positions)
    for n in range(min(positions), max(positions)) :
        fuel = try_function(n, positions)
        if fuel < min_fuel :
            min_fuel = fuel
    return min_fuel

def r1(a) :
    return brut_force(a, try_position)

def r2(a) :
    return brut_force(a, try_position2)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_try_position(self):
        self.assertEqual(try_position(2, example), 37)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
