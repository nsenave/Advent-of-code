import os.path
import unittest
import time

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return f.read().split('\n')



class ArrowKeyboard:

    def __init__(self, next_keyboard):
        self.layout = [
            ['X', '^', 'A'],
            ['<', 'v', '>']
        ]
        self.pos = (0, 2)
        self.next_keyboard = next_keyboard
        self.record = []

    def print_record(self):
        print(''.join(self.record))

    def push_sequence(self, input_sequence: str):
        for input in input_sequence:
            self.push(input)

    def push(self, input: str):
        if input not in "^<>vA":
            raise ValueError(f"Unknown input {input}")
        if input == '^':
            self.next_keyboard.move_up()
        if input == 'v':
            self.next_keyboard.move_down()
        if input == '>':
            self.next_keyboard.move_right()
        if input == '<':
            self.next_keyboard.move_left()
        if input == 'A':
            self.next_keyboard.push_aimed()
        self.record.append(input)
    
    def push_aimed(self):
        i, j = self.pos
        self.push(self.layout[i][j])

    def move_up(self):
        i, j = self.pos
        if i == 0:
            raise IndexError("Cannot move up")
        if j == 0:
            raise SystemError("EXPLOSION")
        self.pos = (i - 1, j)

    def move_down(self):
        i, j = self.pos
        if i == 1:
            raise IndexError("Cannot move down")
        self.pos = (i + 1, j)
    
    def move_right(self):
        i, j = self.pos
        if j == 2:
            return IndexError("Cannot move right")
        self.pos = (i, j + 1)

    def move_left(self):
        i, j = self.pos
        if j == 0:
            return IndexError("Cannot move left")
        if i == 0 and j == 1:
            raise SystemError("EXPLOSION")
        self.pos = (i, j - 1)



class DigitKeyboard:

    def __init__(self):
        self.layout = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['X', '0', 'A'],
        ]
        self.pos = (3, 2)
        self.record = []

    def print_record(self):
        print(''.join(self.record))
    
    def push_aimed(self):
        i, j = self.pos
        self.record.append(self.layout[i][j])

    def move_up(self):
        i, j = self.pos
        if i == 0:
            raise IndexError("Cannot move up")
        self.pos = (i - 1, j)

    def move_down(self):
        i, j = self.pos
        if i == 3:
            raise IndexError("Cannot move down")
        if j == 0:
            raise SystemError("EXPLOSION")
        self.pos = (i + 1, j)
    
    def move_right(self):
        i, j = self.pos
        if j == 2:
            return IndexError("Cannot move right")
        self.pos = (i, j + 1)

    def move_left(self):
        i, j = self.pos
        if j == 0:
            return IndexError("Cannot move left")
        if i == 3 and j == 1:
            raise SystemError("EXPLOSION")
        self.pos = (i, j - 1)



def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    robot0 = DigitKeyboard()
    robot1 = ArrowKeyboard(robot0)
    robot2 = ArrowKeyboard(robot1)
    me = ArrowKeyboard(robot2)
    me.push_sequence("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
    me.print_record()
    robot2.print_record()
    robot1.print_record()
    robot0.print_record()
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
    #print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
