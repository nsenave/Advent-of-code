import unittest
from copy import deepcopy

def line_split(line) :
    return tuple(map(eval, line.split('\n')))

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n\n')))

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)
print("Last pair in input:")
print(puzzle[-1])



def compare_int(left:int, right:int) :
    if left < right :
        return True
    elif left > right :
        return False
    else :
        print("You should not get there")
        return None

def compare_list(left:list, right:list) :
    while len(right) > 0 :
        if len(left) == 0 :
            return True
        else :
            a = left.pop(0)
            b = right.pop(0)
            if a != b :
                return compare(a, b)
    if len(left) > 0 :
        return False

def compare_mixed(left, right) :
    if type(left) == int :
        assert type(right) == list, "Type right should be list here"
        return compare_list([left], right)
    elif type(right) == int :
        assert type(left) == list, "Type left should be list here"
        return compare_list(left, [right])
    else :
        raise ValueError(f"Mixed type comparison called with types {type(left)} and {type(right)}.")

def compare(left, right) :
    if type(left) == int and type(right) == int :
        return compare_int(left, right)
    elif type(left) == list and type(right) == list :
        return compare_list(left, right)
    else :
        return compare_mixed(left, right)

def compare_pair(pair:tuple) :
    left, right = pair
    return compare(left, right)

def r1(a) :
    pairs = deepcopy(a)
    res = 0
    for i in range(len(pairs)) :
        if compare_pair(pairs[i]) :
            res += i+1
    return res



def r2(a) :
    return None



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.example = deepcopy(example)

    def test_compare(self) :
        self.assertTrue(compare([1,2],[3,4]))

    def test_compare_on_example(self):
        self.assertTrue(compare_pair(self.example[0]))
        self.assertTrue(compare_pair(self.example[1]))
        self.assertFalse(compare_pair(self.example[2]))
        self.assertTrue(compare_pair(self.example[3]))
        self.assertFalse(compare_pair(self.example[4]))
        self.assertTrue(compare_pair(self.example[5]))
        self.assertFalse(compare_pair(self.example[6]))
        self.assertFalse(compare_pair(self.example[7]))
    
    def test_compare_with_skip_cases(self) :
        self.assertTrue(compare([1,2,[7,7,7],3], [1,2,[7,7,7],4]))
        self.assertFalse(compare([1,2,[7,7,7],5], [1,2,[7,7,7],4]))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}") # 5967 low # 6298 high
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    # print(f"Puzzle answer:  {r2(puzzle)}")
