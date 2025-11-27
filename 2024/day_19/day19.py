import os.path
import unittest
import time

def line_split(raw_input: str) :
    stripes, designs = raw_input.split('\n\n')
    return stripes.split(', '), designs.split('\n')

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return line_split(f.read())



def is_possible(design, stripes, cache, i=0, debug=False):
    remaining = design[i:]
    if remaining not in cache:
        if debug:
            print(f"Index = {i}")
        if i == len(design) :
            return True
        for stripe in stripes:
            stripe_length = len(stripe)
            if i + stripe_length > len(design) :
                if debug:
                    print(f"Stripe {stripe} is too long")
                continue
            if design[i : i + stripe_length] == stripe:
                if debug:
                    print(f"Stripe {stripe} matches")
                res = is_possible(design, stripes, cache, i + stripe_length, debug)
                if res:
                    return res
        cache.append(remaining)
    return False

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    stripes, designs = puzzle_input
    total = len(designs)
    count = 0
    for design in designs :
        cache = []
        foo = is_possible(design, stripes, cache)
        if debug:
            print(f"Is design {design} possible? {foo}")
        count += 1
        #print(f"Progression {count}/{total}")
        res += foo
    return res



def is_possible2(design, stripes, cache, i=0, debug=False):
    remaining = design[i:]
    if remaining in cache:
        return 0
    res = 0
    if debug:
        print(f"Index = {i}")
    if i == len(design) :
        return 1
    for stripe in stripes:
        stripe_length = len(stripe)
        if i + stripe_length > len(design) :
            continue
        if design[i : i + stripe_length] == stripe:
            res += is_possible2(design, stripes, cache, i + stripe_length, debug)
    if res > 0:
        cache.append(remaining)
    return res

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    stripes, designs = puzzle_input
    total = len(designs)
    count = 0
    for design in designs :
        cache = []
        foo = is_possible2(design, stripes, cache)
        if debug:
            print(f"How many possibilities for {design}? {foo}")
        count += 1
        if count%10 == 0:
            print(f"Progression {count}/{total}")
        res += foo
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.stripes1 = "r, wr, b, g, bwu, rb, gb, br".split(", ")

   # def test(self):
   #     self.assertTrue(is_possible("bwurrg", self.stripes1, debug=True))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')

    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
