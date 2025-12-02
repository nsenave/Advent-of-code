import os.path
import unittest
import time

def line_split(line: str) :
    return tuple(map(int, line.split('-')))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split(',')))



def strict_divisors(n: int) -> list:
    res = [1]
    for d in range(2, n//2 + 1):
        if n % d == 0:
            res.append(d)
    return res

def all_match(pattern, window, id, id_length):
    for i in range(window, id_length, window):
        if id[i : i+window] != pattern:
            return False
    return True

def is_invalid2(id: str) -> bool:
    id_length = len(id)
    for window in strict_divisors(id_length):
        pattern = id[:window]
        if all_match(pattern, window, id, id_length):
            return True
    return False

def is_invalid(id: str) -> bool:
    id_length = len(id)
    if id_length % 2 != 0:
        return False
    half = id_length // 2
    return id[:half] == id[half:]

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for x in puzzle_input :
        for int_id in range(x[0], x[1] + 1):
            if (is_invalid(str(int_id))):
                res += int_id
    return res



def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    invalid_ids = []
    for x in puzzle_input :
        for int_id in range(x[0], x[1] + 1):
            if (is_invalid2(str(int_id))):
                invalid_ids.append(int_id)
    if debug:
        print(f"Invalid ids: {invalid_ids}")
    result = sum(invalid_ids)
    assert result == sum(set(invalid_ids)), "Not a matter of duplicates"
    return result



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_invalid_ids(self):
        for int_id in (11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859):
            id = str(int_id)
            self.assertTrue(is_invalid(id))

    def test_valid_ids(self):
        # 565653-565659,824824821-824824827,2121212118-2121212124
        for int_id in range(565653, 565659):
            id = str(int_id)
            if is_invalid(id):
                print(id)
            self.assertFalse(is_invalid(id))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')
    if puzzle is not None:
        print(f"Real input: [{puzzle[0]}, ..., {puzzle[-1]}]")

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
