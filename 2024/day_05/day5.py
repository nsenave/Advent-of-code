import os.path
import unittest
import time

def line_split(line: str) :
    return tuple(map(int, line.split("|")))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        rules, updates = f.read().split('\n\n')
        return list(map(line_split, rules.split("\n"))), list(map(lambda line: list(map(int,line.split(","))), updates.split("\n")))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example[0])
print(example[1])



def create_index(rules: list) :
    index = {}
    for rule in rules:
        left = rule[0]
        right = rule[1]
        if left not in index:
            index[left] = []
        index[left].append(right)
    return index

def is_valid_update(update: list, rules_map: dict, debug=False) -> bool:
    printed_pages = []
    for page in update :
        for printed_page in printed_pages :
            if page not in rules_map :
                continue
            if printed_page in rules_map[page] :
                if debug :
                    print(f"Page {page} cannot be printed, must be before {printed_page}.")
                return False
        printed_pages.append(page)
    return True

def get_middle_page(update: list) -> int:
    return update[len(update) // 2]

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    rules, updates = puzzle_input
    rules_map = create_index(rules)
    if debug :
        print(rules_map)
    res = 0
    for update in updates :
        is_valid = is_valid_update(update, rules_map, debug)
        if debug :
            print(f"Update {update} is valid? {is_valid}")
        if is_valid:
            res += get_middle_page(update)
    return res



def sort_update(update: list, rules: list, rules_map: dict) -> None:
    while not is_valid_update(update, rules_map):
        length = len(update)
        for i in range(length):
            for j in range(i+1, length):
                if (update[j], update[i]) in rules:
                    update[j], update[i] = update[i], update[j]

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    rules, updates = puzzle_input
    rules_map = create_index(rules)
    #
    invalid_updates = []
    for update in updates :
        if not is_valid_update(update, rules_map, False):
            invalid_updates.append(update)
    #
    for update in invalid_updates:
        if debug :
            print(f"Before sorting: {update}")
        sort_update(update, rules, rules_map)
        if debug :
            print(f"After sorting:  {update}")
    #
    return sum(map(get_middle_page, invalid_updates))



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(r1(example), 143)
        self.assertEqual(get_middle_page([1,2,3]), 2)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")
    
    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
