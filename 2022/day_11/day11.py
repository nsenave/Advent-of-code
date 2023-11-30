import unittest
from copy import deepcopy



class Monkey :
    def __init__(self, expression:str, test_value:int, target_true:int, target_false:int) :
        self.items = []
        self.operation = lambda old: eval(expression)
        self.test_value = test_value
        self.target_true = target_true
        self.target_false = target_false
    def add_item(self, item:int) :
        self.items.append(item)
    def has_item(self) :
        return len(self.items) > 0
    def inspect(self) -> int :
        item = self.items.pop(0)
        return self.operation(item) // 3
    def inspect2(self, lcm) -> int :
        item = self.items.pop(0)
        return self.operation(item) % lcm
    def test(self, item:int) -> bool :
        return item % self.test_value == 0
    def target(self, item:int) -> int :
        return self.target_true if self.test(item) else self.target_false
    def __str__(self) :
        return f"Monkey: {self.items}"



def parse_monkey(string) :
    lines = string.split('\n')
    expression = lines[2].split(' = ')[1]
    test_value = int(lines[3].split(' ')[-1])
    target_true = int(lines[4].split(' ')[-1])
    target_false = int(lines[5].split(' ')[-1])
    monkey = Monkey(expression, test_value, target_true, target_false)
    for s in lines[1].split(': ')[1].split(', ') :
        monkey.add_item(int(s))
    return monkey

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return list(map(parse_monkey, f.read().split('\n\n')))

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
for monkey in example : print(monkey)



def throw(monkey: Monkey, monkeys: list) :
    inspected_item = monkey.inspect()
    target_monkey = monkeys[monkey.target(inspected_item)]
    target_monkey.add_item(inspected_item)

def monkey_business(counts: list) -> int :
    first = max(counts)
    counts.remove(first)
    second = max(counts)
    return first * second

def r1(a: list, debug=False) :
    monkeys = deepcopy(a)
    monkeys_number = len(monkeys)
    throw_counts = [0 for n in range(monkeys_number)]
    for round in range(1,20+1) :
        for n in range(monkeys_number) :
            monkey = monkeys[n]
            while monkey.has_item() :
                throw(monkey, monkeys)
                throw_counts[n] += 1
        if debug :
            if 1<=round<=10 or round in (15,20) :
                print(f"After round {round}:")
                for monkey in monkeys : print(monkey)
    print(throw_counts)
    return monkey_business(throw_counts)



def throw2(monkey: Monkey, lcm:int, monkeys: list) :
    inspected_item = monkey.inspect2(lcm)
    target_monkey = monkeys[monkey.target(inspected_item)]
    target_monkey.add_item(inspected_item)

def r2(a: list, debug=False) :
    monkeys = deepcopy(a)
    # Least common multiple = product since test values are prime
    lcm = 1
    for monkey in monkeys :
        lcm *= monkey.test_value
    #
    monkeys_number = len(monkeys)
    throw_counts = [0 for n in range(monkeys_number)]
    for round in range(1, 10000+1) :
        for n in range(monkeys_number) :
            monkey = monkeys[n]
            while monkey.has_item() :
                throw2(monkey, lcm, monkeys)
                throw_counts[n] += 1
        if debug :
            if round in (1,20) or (round)%1000 == 0 :
                print(f"After round {round}: {throw_counts}")
        else :
            if (round)%1000 == 0 :
                print(f"Round {round} finished.")
    return monkey_business(throw_counts)




class TestsOfToday(unittest.TestCase):

    def setUp(self):
        self.op1 = lambda old: eval('old * 3')
        self.test_monkey = example[0]

    def test(self):
        self.assertEqual(15, self.op1(5))
    
    def test_monkey_parsing(self) :
        self.assertEqual(23, self.test_monkey.test_value)
        self.assertEqual(2, self.test_monkey.target_true)
        self.assertEqual(3, self.test_monkey.target_false)
        self.assertEqual(19, self.test_monkey.operation(1))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
