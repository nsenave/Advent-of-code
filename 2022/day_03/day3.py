import unittest

def line_split(line) :
    res = line
    return res

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))[:-1]

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def priority(char: str) -> int :
    i = ord(char)
    return i-96 if i>=97 else i-38

def split_rucksacks(rucksacks: str) :
    r_size = len(rucksacks)//2
    return (rucksacks[:r_size], rucksacks[r_size:])

def r1(a) :
    res = 0
    for rucksacks in a :
        r_size = len(rucksacks)//2
        r1 = rucksacks[:r_size]
        r2 = rucksacks[r_size:]
        for c in set(r1) :
            if c in r2 :
                res += priority(c)
    return res



def r2(a) :
    res = 0
    k = 0
    rucksacks_count = len(a)
    while k < rucksacks_count :
        e1 = a[k]
        e2 = a[k+1]
        e3 = a[k+2]
        for c in set(e1) :
            if (c in e2) and (c in e3) :
                res += priority(c)
                print(c, priority(c))
        k += 3
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_split_rucksacks(self):
        self.assertEqual(split_rucksacks("vJrwpWtwJgWrhcsFMMfFFhFp"), ("vJrwpWtwJgWr", "hcsFMMfFFhFp"))
    
    def test_priority(self):
        self.assertEqual(priority('a'), 1)
        self.assertEqual(priority('z'), 26)
        self.assertEqual(priority('A'), 27)
        self.assertEqual(priority('Z'), 52)
    
    def test_input_size(self) :
        self.assertTrue(len(puzzle)%3 == 0)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
