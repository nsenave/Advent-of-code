import os.path
import unittest
import time



def check(a, b):
    """Checks that button A and B are not a multiple from each other"""
    xa, ya = a
    xb, yb = b
    if (xa >= xb and xa % xb == 0 and xa // xb == ya // yb) or \
        (xb % xa == 0 and xb // xa == yb // ya):
        raise ValueError("Button A and B are multiples.")

class Machine:
    def __init__(self, a: tuple, b: tuple, price_location: tuple):
        check(a, b)
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



MAX_PRESS = 100

def press_buttons(machine: Machine, a_press, b_press):
    return (machine.a[0] * a_press + machine.b[0] * b_press, machine.a[1] * a_press + machine.b[1] * b_press)

def is_solution(x, y, machine: Machine):
    x_prize, y_prize = machine.prize_location
    if x > x_prize or y > y_prize:
        return 1 # too high
    if x < x_prize or y < y_prize:
        return -1 # too low
    return 0 # ok

def find_solutions(machine):
    res = []
    too_high = False
    a_press = 0
    while a_press <= MAX_PRESS: # and not too_high:
        b_press = 0
        while b_press <= MAX_PRESS: # and not too_high:
            x, y = press_buttons(machine, a_press, b_press)
            result = is_solution(x, y, machine)
            if result == 1:
                too_high = True
            if result == 0:
                res.append((a_press, b_press))
            b_press += 1
        a_press += 1
    return res

def tokens_count(combination):
    return 3 * combination[0] + combination[1]

def lowest_solution(combinations):
    if not combinations:
        return None
    res = combinations[0]
    lowest = tokens_count(res)
    for k in range(1, len(combinations)):
        combination = combinations[k]
        count = tokens_count(combination)
        if count < lowest:
            res = combination
            lowest = count
    return res

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for machine in puzzle_input :
        solutions = find_solutions(machine)
        lowest = lowest_solution(solutions)
        if len(solutions) > 1:
            print("Several solutions")
        if debug:
            print(lowest)
        if lowest is not None:
            res += tokens_count(lowest)
    return res



def decomp(number, x1, x2):
    res = []
    for k1 in range(number // x1 + 1):
        for k2 in range(number // x2 + 1):
            if k1 * x1 + k2 * x2 == number:
                res.append((k1, k2))
    return res

def find_solution2(machine: Machine):
    xa, xb = machine.a
    ya, yb = machine.b
    x_price, y_price = machine.prize_location
    for ka in range(x_price // xa + 1):
        for kb in range(x_price // xb + 1):
            if ka * xa + kb * xb == x_price and ka * ya + kb * yb == y_price:
                return ka, kb
    return None

def machine2(machine: Machine):
    prize_location2 = (10000000000000 + machine.prize_location[0], \
                       10000000000000 + machine.prize_location[1])
    return Machine(machine.a, machine.b, prize_location2)

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for machine in puzzle_input :
        solution = find_solution2(machine2(machine))
        if solution is not None:
            res += tokens_count(solution)
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_press_buttons(self):
        machine = Machine((1, 2), (3, 5), (6, 11))
        self.assertEqual((1, 2), press_buttons(machine, 1, 0))
        self.assertEqual((3, 5), press_buttons(machine, 0, 1))
        self.assertEqual((6, 11), press_buttons(machine, 3, 1))
        self.assertEqual(0, is_solution(6, 11, machine))

    def test_decomp(self):
        self.assertEqual(set([(16, 0), (11, 1), (6, 2), (1, 3)]), set(decomp(16, 1, 5)))

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
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
