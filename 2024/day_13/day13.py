import os.path
import unittest
import time

class Machine:
    def __init__(self, a: tuple, b: tuple, price_location: tuple):
        self.a = a
        self.b = b
        self.prize_location = price_location
    def __str__(self):
        return f"""
Button A: {self.a}
Button B: {self.b}
Prize location: {self.prize_location}"""

def parse_button(button_instruction: str):
    x_instruction, y_instruction = button_instruction[10:].split(", ")
    return int(x_instruction[2:]), int(y_instruction[2:])

def parse_prize(prize: str):
    x_location, y_loaction = prize[7:].split(", ")
    return int(x_location[2:]), int(y_loaction[2:])

def parse_configuration(configuration: str) :
    buttonA, buttonB, prize = configuration.split('\n')
    return Machine(parse_button(buttonA), parse_button(buttonB), parse_prize(prize))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(parse_configuration, f.read().split('\n\n')))



def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for x in puzzle_input :
        pass
    return res



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
    for machine in example:
        print(machine)

    puzzle = parse_input('input.txt')

    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    #print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
