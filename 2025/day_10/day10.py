import os.path
import unittest
import time
import itertools


def parse_button(str_button):
    return tuple(map(int, str_button[1:-1].split(',')))

def line_split(line: str) -> tuple:
    parts = line.split(' ')
    indicator_lights = parts[0][1:-1]
    buttons = list(map(parse_button, parts[1:-1]))
    joltages = list(map(int, parts[-1][1:-1].split(',')))
    return (indicator_lights, buttons, joltages)

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))



# Press 0 button, then 1 button, then 2 buttons etc.
def ordered_inputs(buttons_number):
    """Yields lists of inputs (press button at index i or not)"""
    yield [False] * buttons_number
    for press_number in range(1, buttons_number + 1):
        for positions in itertools.combinations(range(buttons_number), press_number):
            inputs = [False] * buttons_number
            for p in positions:
                inputs[p] = True
            yield inputs

def init_lights(buttons_number):
    """Returns list of initial light values (all False i.e. off)."""
    return [False] * buttons_number

def bool_value(indicator_light: str):
    return indicator_light == '#'

def press_button(button: tuple, lights: list):
    for i in button:
        lights[i] = not lights[i]

def apply(inputs, buttons, lights):
    for press, button in zip(inputs, buttons):
        if press:
            press_button(button, lights)

def matches_indicator(lights: list, indicator_lights: str) -> bool:
    for indicator_light, light in zip(indicator_lights, lights):
        if bool_value(indicator_light) != light:
            return False
    return True

def find_min_press_number(x):
    indicator_lights, buttons, _ = x
    lights_length = len(indicator_lights)
    buttons_number = len(buttons)
    for inputs in ordered_inputs(buttons_number):
        lights = init_lights(lights_length)
        apply(inputs, buttons, lights)
        if matches_indicator(lights, indicator_lights):
            return sum(inputs)

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
    print(example)

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
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
