import unittest

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return f.read()

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def first_marker(message: str, length: int) -> int :
    res = length
    current = list(message[:length])
    for c in message[length:] :
        if len(set(current)) == length :
            return res
        current.pop(0)
        current.append(c)
        res += 1

def r1(a) :
    return first_marker(a, 4)



def r2(a) :
    return first_marker(a, 14)



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
