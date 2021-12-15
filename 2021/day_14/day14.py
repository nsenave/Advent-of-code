import unittest
from copy import deepcopy

def line_split(line) :
    res = line
    return res

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        polymer, rules_raw = f.read().split('\n\n')
        rules = {line[:2]:line[6] for line in rules_raw.split('\n')}
        return polymer, rules

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def step(polymer, rules) :
    res = polymer[0]
    for i in range(len(polymer) - 1) :
        rule = rules[polymer[i:i+2]]
        res += rule + polymer[i+1]
    return res

def r1(a) :
    polymer, rules = a
    for N in range(10) :
        polymer = step(polymer, rules)
    counts = list(map(lambda s: polymer.count(s), set(list(polymer))))
    print(counts)
    return max(counts) - min(counts)



def get_letters(rules) :
    res = set()
    for pair in rules.keys() :
        res.update(set(list(pair)))
    return res

def pair_occurrences(polymer:str, rules:dict) -> dict :
    res = {pair:0 for pair in rules}
    for i in range(len(polymer) - 1) :
        res[polymer[i:i+2]] += 1
    return res

def step2(occurrences:dict, rules) -> dict :
    """occurrences[pair] = occurrences of that pair"""
    res = deepcopy(occurrences)
    for pair in occurrences :
        if occurrences[pair] > 0 :
            n = occurrences[pair]
            rule = rules[pair]
            res[ pair ] -= n
            res[ pair[0] + rule ] += n
            res[ rule + pair[1] ] += n
    return res

def get_count_from_occurrences(occurrences:dict, first_letter:str, last_letter:str, rules:dict) -> dict :
    """Return the number of occurrences of each letter given the number of occurrences of pairs 
    and the polymer first and last letter. Rules are used to get the list of letters."""
    res = {letter:0 for letter in get_letters(rules)}
    for pair in occurrences :
        n = occurrences[pair]
        res[pair[0]] += n
        res[pair[1]] += n
    for letter in res :
        if letter in (first_letter, last_letter) :
            res[letter] = (res[letter]+1) // 2
        else :
            res[letter] //= 2
    return res

def step_over2(N, occurrences:dict, rules) -> dict :
    """apply N times step2"""
    for n in range(N) :
        occurrences = step2(occurrences, rules)
    return occurrences

def r2(a) :
    polymer, rules = a
    occurrences = pair_occurrences(*a)
    for N in range(40) :
        occurrences = step2(occurrences, rules)
    counts = list(get_count_from_occurrences(occurrences, polymer[0], polymer[-1], rules).values())
    return max(counts) - min(counts)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.example_polymers = [
            "NCNBCHB",
            "NBCCNBBBCBHCB",
            "NBBBCNCCNBBNBNBBCHBHHBCHB",
            "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
        ]
    
    def test_step2(self) :
        polymer, rules = example
        occurrences = pair_occurrences(*example)
        for N in range(4) :
            occurrences = step2(occurrences, rules)
            self.assertDictEqual(occurrences, pair_occurrences(self.example_polymers[N], rules))
    
    def test_count_letters(self) :
        polymer, rules = example
        occurrences = pair_occurrences(polymer, rules)
        letters10 = get_count_from_occurrences(step_over2(10, occurrences, rules), 'N', 'B', rules)
        self.assertEqual(letters10['B'], 1749)
        self.assertEqual(letters10['C'], 298)
        self.assertEqual(letters10['H'], 161)
        self.assertEqual(letters10['N'], 865)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
