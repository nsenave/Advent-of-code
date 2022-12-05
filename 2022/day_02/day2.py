import unittest

def convert_letter(letter) :
    return 1 if letter in ('A','X') else 2 if letter in ('B','Y') else 3

def line_split(line) :
    res = tuple(map(convert_letter, line.split(' ')))
    return res

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))[:-1]

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def turn_score(turn: tuple) -> int :
    turn_res = turn[0] - turn[1]
    return 6 if turn_res in (-1,2) else 3 if turn_res == 0 else 0

def r1(a) :
    score = 0
    for turn in a :
        score += turn[1] + turn_score(turn)
    return score



def win(t: int) -> int :
    return 1 if t == 3 else t+1
def lose(t: int) -> int :
    return 3 if t == 1 else t-1

def r2(a) :
    score = 0
    for turn in a :
        t0, t1 = turn
        score += 6 + win(t0) if t1 == 3 else 3 + t0 if t1 == 2 else 0 + lose(t0)
    return score



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(turn_score((1,1)), 3)
        self.assertEqual(turn_score((1,2)), 6)
        self.assertEqual(turn_score((1,3)), 0)
        self.assertEqual(turn_score((2,1)), 0)
        self.assertEqual(turn_score((2,2)), 3)
        self.assertEqual(turn_score((2,3)), 6)
        self.assertEqual(turn_score((3,1)), 6)
        self.assertEqual(turn_score((3,2)), 0)
        self.assertEqual(turn_score((3,3)), 3)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
