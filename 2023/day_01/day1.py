import unittest
import os.path

def line_split(line: str) :
    res = line
    return res

def parse_input(file_path: str) :
    if os.path.exists(file_path) :
        with open(file_path, 'r') as f :
            return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def add_char_if_number(numbers, c):
    n = ord(c)
    if 48 <= n < 58 :
        numbers[-1].append(c)

def add_number_chars(numbers, line):
    for c in line :
        add_char_if_number(numbers, c)

def compute_result(numbers):
    result = 0
    for line in numbers :
        result += int(line[0] + line[-1])
    return result

def r1(a) :
    if a is None :
        return None
    numbers = []
    for line in a :
        numbers.append([])
        add_number_chars(numbers, line)
    return compute_result(numbers)



puzzle2 = parse_input('input2.txt')
example2 = parse_input('input2-example.txt')

NUMBERS_DICT = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'zero': '0'
        }

print("Example input 2:")
print(example2)

def r2(a, is_example=False) :
    if a is None :
        return None
    numbers = []
    for line in a :
        numbers.append([])
        char_window = ''
        for c in line :
            char_window += c
            for char_number in NUMBERS_DICT:
                if char_number in char_window :
                    numbers[-1].append(NUMBERS_DICT[char_number])
                    char_window = char_window[-1] # keeping the last character as it can be in two number words
            add_char_if_number(numbers, c)
    if is_example :
        print(numbers)
    return compute_result(numbers)



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
    print(f"Example result: {r2(example2, True)}")
    print(f"Puzzle answer:  {r2(puzzle2)}")
