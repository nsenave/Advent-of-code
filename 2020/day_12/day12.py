import os.path
import unittest

# Order in
DIRECTIONS = ['N', 'E', 'S', 'W']
FORWARD = 'F'
RIGHT = 'R'
LEFT = 'L'

def line_split(line: str) :
    instruction, number = line[0], int(line[1:])
    return instruction, number

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def update_direction(current_direction: str, instruction: str, number: int) -> str :
    if number%90 != 0 :
        raise ValueError(f"Degree of a turn must be a multiple of 45, invalid input given: {number}")
    current_index = DIRECTIONS.index(current_direction)
    if instruction == RIGHT :
        return DIRECTIONS[(current_index + (number//90)) % 4]
    if instruction == LEFT :
        return DIRECTIONS[(current_index - (number//90)) % 4]

def move_forward(coords: tuple, current_direction: str,  number: int) -> tuple :
    return move_from_direction(coords, current_direction, number);

def move_from_direction(coords: tuple, direction: str, number: int) -> tuple :
    x,y = coords
    if direction == 'N' :
        return (x-number, y)
    if direction == 'E' :
        return (x, y+number)
    if direction == 'S' :
        return (x+number, y)
    if direction == 'W' :
        return (x, y-number)

def apply_instruction(coords, current_direction, instruction, number):
    if instruction in DIRECTIONS:
        coords = move_from_direction(coords, instruction, number)
        return coords, current_direction
    if instruction == FORWARD:
        coords = move_forward(coords, current_direction, number)
        return coords, current_direction
    if instruction in (RIGHT, LEFT):
        current_direction = update_direction(current_direction, instruction, number)
        return coords, current_direction
    raise ValueError(f"Unexpected instruction type: '{instruction}'")

def r1(a) :
    if a is None :
        return None
    coords = (0, 0)
    current_direction = 'E'
    for instruction, number in a:
        coords, current_direction = apply_instruction(coords, current_direction, instruction, number)
    return sum(map(abs, coords))



def move_to_waypoint(ship_coords: tuple, waypoint_coords: tuple, number: int) :
    vertical_dist = (waypoint_coords[0] - ship_coords[0]) * number
    horizontal_dist = (waypoint_coords[1] - ship_coords[1]) * number
    return (ship_coords[0] + vertical_dist, ship_coords[0] + horizontal_dist), (waypoint_coords[0] + vertical_dist, waypoint_coords[0] + horizontal_dist)

def rotate_waypoint(ship_coords: tuple, waypoint_coords: tuple, instruction: str, number: int) :
    vertical_dist = waypoint_coords[0] - ship_coords[0]
    horizontal_dist = waypoint_coords[1] - ship_coords[1]

def r2(a) :
    if a is None :
        return None
    return None



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual('E', update_direction('N', 'R', 90))
        self.assertEqual('S', update_direction('N', 'R', 180))
        for direction in DIRECTIONS:
            self.assertEqual(update_direction(direction, 'R', 180), update_direction(direction, 'L', 180))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    # print(f"Puzzle answer:  {r2(puzzle)}")
