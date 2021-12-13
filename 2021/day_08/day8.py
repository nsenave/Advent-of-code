import unittest

def line_split(line) :
    return tuple(map(lambda x: x.split(' '), line.split(' | ')))

with open('input.txt', 'r') as f :
    puzzle = list(map(line_split, f.read().split('\n')))

with open('example/input.txt', 'r') as f :
    example = list(map(line_split, f.read().split('\n')))

print("Example input:")
print(example)

display_example = ('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab'.split(' '), 'cdfeb fcadb cdfeb cdbaf'.split(' '))
print("First example:")
print(display_example)



def r1(a) :
    res = 0
    for display in a :
        digits = display[1]
        for d in digits :
            if len(d) in (2,4,3,7) :
                res += 1
    return res



segments_number = {
    0:6, 1:2, 2:5, 3:5, 4:4, 5:5, 6:6, 7:3, 8:7, 9:6
}

def all_in(d:str, d2:str) -> bool :
    """Return true if all characters of d are in d2"""
    for c in d :
        if c not in d2 :
            return False
    return True

def uncommon(s1:str, s2:str) -> str :
    """Return a string contining common characters of s1 and s2"""
    res = ""
    for c in s1 :
        if c not in s2 :
            res += c
    for c in s2 :
        if c not in s1 :
            res += c
    return res

def remove_incompatibles(connexions, d, matching, incompatibles) :
    connexions[matching] = [d]
    for n in incompatibles :
        k = 0
        while k < len(connexions[n]) :
            d2 = connexions[n][k]
            if all_in(d, d2) :
                if d2 in connexions[n] :
                    connexions[n].remove(d2)
                else :
                    k += 1
            else :
                k += 1

def resolve_pattern(pattern) :
    connexions = {}
    #
    for i in range(10) :
        connexions[i] = []
        for d in pattern :
            if len(d) == segments_number[i] :
                connexions[i].append(d)
    #
    for d in pattern :
        if len(d) == 2 : 
            remove_incompatibles(connexions, d, 1, (2,5,6))
        elif len(d) == 4 :
            remove_incompatibles(connexions, d, 4, (0,2,3,5,6))
        elif len(d) == 3 :
            remove_incompatibles(connexions, d, 7, (2,5,6))
        elif len(d) == 7 :
            connexions[8] = [d]
    #
    bbbb_dddd = uncommon(connexions[1][0], connexions[4][0])
    remove_incompatibles(connexions, bbbb_dddd, -1, (0,2,3))
    #
    k = 0
    while k < len(connexions[5]) :
        d = connexions[5][k]
        if not all_in(d, connexions[6][0]) :
            connexions[5].remove(d)
        else :
            k += 1
    #
    for n in (2,5) :
        d = connexions[n][0]
        if d in connexions[3] :
            connexions[3].remove(d)
    for n in (0,6) :
        d = connexions[n][0]
        if d in connexions[9] :
            connexions[9].remove(d)
    #
    return connexions

def sort_string(s) :
    return ''.join(sorted(s))

def get_display_digits(display) :
    connexions = resolve_pattern(display[0])
    mapping = {sort_string(v[0]): k for k, v in connexions.items()}
    res = ''
    for d in display[1] :
        try :
            res += str(mapping[sort_string(d)])
        except KeyError :
            print(connexions)
            print(mapping)
            print(display[1])
    return int(res)

def r2(a) :
    return sum(map(get_display_digits, a))



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_all_in(self):
        self.assertTrue(all_in('gf','gcf'))
        self.assertTrue(all_in('ab','dsqbhjka'))
        self.assertFalse(all_in('ab','acefg'))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(resolve_pattern(display_example[0]))
    print(get_display_digits(display_example))
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
