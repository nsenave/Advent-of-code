from typing import Iterable
import unittest
from copy import deepcopy

def line_split(line) :
    return line

with open('input.txt', 'r') as f :
    puzzle = list(map(line_split, f.read().split('\n')))

with open('example/input.txt', 'r') as f :
    example = list(map(line_split, f.read().split('\n')))

print("Example input:")
print(example)
print('')


pairs = ('[]', r'{}', '()', '<>')
pairs_dict = {
    '{':'}',
    '[':']',
    '(':')',
    '<':'>'
}
closings = list(pairs_dict.values())
scores_dict = {
    '}':1197,
    ']':57,
    ')':3,
    '>':25137
}

def any_of(values:Iterable[str], s:str) :
    for value in values :
        if value in s :
            return True
    return False

def simplify(chunk:str) :
    while any_of(pairs, chunk) :
        for pair in pairs :
            while pair in chunk :
                chunk = chunk.replace(pair, '')
    return chunk

def is_corrupted(chunk:str) -> bool :
    """corrupted or incomplete simplified chunk"""
    for c in chunk :
        if c in closings :
            return True
    return False

def first_incorrect(chunk, do_simplify=True) :
    if do_simplify :
        chunk = simplify(chunk)
    i = 0
    while chunk[i] not in closings :
        i += 1
    return chunk[i]

def score(chunk) :
    chunk = simplify(chunk)
    if is_corrupted(chunk) :
        return scores_dict[first_incorrect(chunk, False)]
    else :
        return 0

def r1(a) :
    """a = chunk list"""
    return sum(map(score, a))



scores_dict2 = {
    '}':3,
    ']':2,
    ')':1,
    '>':4
}

def is_incomplete(chunk:str) -> bool :
    """corrupted or incomplete simplified chunk"""
    return not is_corrupted(chunk)

def missing_characters(chunk, do_simplify=True) :
    if do_simplify :
        chunk = simplify(chunk)
    res = []
    for c in chunk :
        res.insert(0, pairs_dict[c])
    return res

def score2(chunk) :
    res = 0
    for c in missing_characters(chunk) :
        res *= 5
        res += scores_dict2[c]
    return res

def r2(a) :
    incompletes = []
    for chunk in a :
        chunk = simplify(chunk)
        if is_incomplete(chunk) :
            incompletes.append(chunk)
    print(incompletes)
    scores = list(map(score2, incompletes))
    return sorted(scores)[len(scores)//2]



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_first_incorrect(self):
        self.assertEqual(first_incorrect('{([(<{}[<>[]}>{[]{[(<()>'), '}')
    
    def test_missing_characters(self) :
        self.assertEqual(missing_characters('[({(<(())[]>[[{[]{<()<>>'), list(r'}}]])})]'))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
