import unittest
from copy import deepcopy



with open('input.txt', 'r') as f :
    puzzle = list(map(int, f.read().split(',')))

with open('example/input.txt', 'r') as f :
    example = list(map(int, f.read().split(',')))

print("Example input:")
print(example)



def next_day(fishes) :
    news = 0
    for k in range(len(fishes)) :
        state=fishes[k]
        if state == 0 :
            fishes[k] = 8
            fishes.append(6)
        else :
            fishes[k] -= 1
    return fishes

def n_days(fishes, days) :
    for d in range(days) :
        next_day(fishes)

def r1(a, days=80) :
    fishes = deepcopy(a)
    n_days(fishes, days)
    return len(fishes)



def f(d, s) : # works but still waay too slow
    if d <= 0 :
        return 1
    else :
        if s == 0 :
            return f(d-7, 0) + f(d-7, 2)
        else :
            return f(d-1, s-1)

def states_after_n_days(fishes, n) :
    states = [0] * 9
    for fish in fishes :
        states[fish] += 1
    for day in range(n) :
        new_fishes = states[0]
        states = states[1:] + [new_fishes]
        states[6] += new_fishes
    return states

def r2(a, days=256) :
    return sum(states_after_n_days(a, days))



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
    print(r2(example, 80))
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
