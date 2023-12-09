import os.path
import unittest

def line_split(line: str) :
    return list(map(int, line.split()))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def is_all_zeros(sequence):
    for value in sequence:
        if value != 0:
            return False
    return True

def compute_differences(sequence: list):
    sequences = [sequence]
    n = len(sequence)
    while not is_all_zeros(sequence):
        differences = []
        for k in range(n-1):
            differences.append(sequence[k+1] - sequence[k])
        sequences.append(differences)
        sequence = differences
        n = n-1
    return(sequences)

def resolve(sequences) -> int:
    next_value = 0
    for sequence in reversed(sequences):
        next_value += sequence[-1]
    return next_value

def resolve_backwards(sequences) -> int:
    next_value = 0
    for sequence in reversed(sequences):
        next_value = sequence[0] - next_value
    return next_value

def find_next_value(sequence: list) -> int:
    return resolve(compute_differences(sequence))

def find_previous_value(sequence: list) -> int:
    return resolve_backwards(compute_differences(sequence))

def r1(a) :
    if a is None :
        return None
    return sum(map(find_next_value, a))



def r2(a) :
    if a is None :
        return None
    return sum(map(find_previous_value, a))



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
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
