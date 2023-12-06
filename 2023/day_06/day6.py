import os.path
import unittest

def line_split(line: str) :
    return list(map(int, line[11:].split()))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)

print("Puzzle input:")
print(puzzle)



def play_race(chosen_speed: int, time_available: int) -> int:
    """Return the distance parcourue during the (counting the time spent at pressing the button)."""
    return (time_available - chosen_speed) * chosen_speed # time spent to press the button = chosen speed

def r1(a) :
    if a is None :
        return None
    times, distances = a
    result = 1
    for time_available, distance in zip(times, distances):
        winning_speed_count = 0
        for chosen_speed in range(1, time_available):
            if play_race(chosen_speed, time_available) > distance:
                winning_speed_count += 1
        result *= winning_speed_count
    return result



def line_split2(line: str) :
    return int(line[11:].replace(' ', ''))

def parse_input2(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return tuple(map(line_split2, f.read().split('\n')))

puzzle2 = parse_input2('input.txt')
example2 = parse_input2('input-example.txt')

print("Example input 2:")
print(example2)

print("Puzzle input 2:")
print(puzzle2)

def delta(time_available:int, distance:int):
    return time_available**2 - 4*distance

def roots(time_available:int, distance:int):
    r1 = (time_available - delta(time_available, distance)**(1/2)) / 2
    r2 = (time_available + delta(time_available, distance)**(1/2)) / 2
    return (r1, r2)

def r2(a) :
    if a is None :
        return None
    time_available, distance = a
    r1, r2 = roots(time_available, distance)
    bound1, bound2 = int(r1), int(r2)
    if play_race(bound1, time_available) < distance:
        bound1 += 1
    if play_race(bound2, time_available) < distance:
        bound2 -= 1
    print(bound1, bound2)
    return (bound2 - bound1) + 1



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example2)}")
    print(f"Puzzle answer:  {r2(puzzle2)}")
