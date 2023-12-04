import os.path
import unittest
import numpy as np

def line_split(line: str) :
    res = list('.' + line + '.')
    return res

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        a_list = list(map(line_split, f.read().split('\n')))
        m = len(a_list[0])
        empty_top_row = ['.' for j in range(m)]
        empty_bottom_row = ['.' for j in range(m)]
        return np.array([empty_top_row] + a_list + [empty_bottom_row])

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def is_number(c: str) -> bool:
    return 48 <= ord(c) < 58

def is_symbol_around(a: np.array, current_i, j1, j2) -> bool:
    for i in (current_i-1, current_i+1) :
        for j in range(j1-1, j2+2) :
            if a[i,j] != '.' :
                return True
    if a[current_i, j1 - 1] != '.' :
        return True
    if a[current_i, j2 + 1] != '.' :
        return True
    return False

def r1(a: np.array) :
    if a is None :
        return None
    result = 0
    n,m = a.shape
    for i in range(n) :
        j = 0
        while j < m :
            current_number = ''
            j0 = j
            while is_number(a[i,j]) :
                current_number += a[i,j]
                j += 1
            else :
                if current_number != '' and is_symbol_around(a, i, j0, j-1) :
                    result += int(current_number)
                #if current_number != '' and not is_symbol_around(a, i, j0, j-1) :
                #    print(current_number)
                j += 1
    return result



def is_number_around(a: np.array, i:int, j:int) -> bool:
    for i in (i-1, i, i+1):
        for j in (j-1, j, j+1) :
            if is_number(a[i,j]) :
                return True
    return False

def find_part_number(a: np.array, i: int, j_gear:int) -> int:
    j = j_gear - 1
    while j < a.shape[1] and not is_number(a[i, j]) :
        j += 1
        if j > j_gear + 1 :
            return None
    j0 = j
    while j < a.shape[1] and j >= 0 and is_number(a[i, j0]) :
        j0 -= 1
    j0 += 1
    j = j0
    while j < a.shape[1] and is_number(a[i, j]) :
        j += 1
    j1 = j
    string_res = " ".join(a[i, j0:j1].tolist()).replace(" ", "")
    if string_res == "" :
        return None
    return int(string_res)

def gear_ratio(a: np.array, i_gear: int, j_gear: int) -> int:
    part_numbers = set()
    part_number_above = find_part_number(a, i_gear-1, j_gear)
    if (part_number_above is not None) and is_number(a[i_gear-1, j_gear+1]) and a[i_gear-1, j_gear] == '.' :
        j = j_gear+1
        other_above_number = ''
        while is_number(a[i_gear-1, j]) :
            other_above_number += a[i_gear-1, j]
            j += 1
        part_numbers.add(int(other_above_number))
    part_number_left = None
    if is_number(a[i_gear, j_gear-1]) :
        part_number_left = find_part_number(a, i_gear, j_gear-1)
    part_number_right = None
    if is_number(a[i_gear, j_gear+1]) :
        part_number_right = find_part_number(a, i_gear, j_gear+1)
    part_number_below = find_part_number(a, i_gear+1, j_gear)
    if (part_number_below is not None) and is_number(a[i_gear+1, j_gear+1]) and a[i_gear+1, j_gear] == '.' :
        j = j_gear+1
        other_below_number = ''
        while is_number(a[i_gear+1, j]) :
            other_below_number += a[i_gear+1, j]
            j += 1
        part_numbers.add(int(other_below_number))
    
    for part_number in [part_number_above, part_number_left, part_number_right, part_number_below] :
        if part_number is not None :
            part_numbers.add(part_number)
    #print(part_numbers)
    if len(part_numbers) != 2 :
        return None
    part_numbers_list = list(part_numbers)
    return part_numbers_list[0] * part_numbers_list[1]

def r2(a) :
    if a is None :
        return None
    result = 0
    n,m = a.shape
    for i in range(1,n-1) :
        for j in range(1,m-1) :
            if a[i,j] == '*' :
                gear_ratio_value = gear_ratio(a, i, j)
                if gear_ratio_value is not None :
                    result += gear_ratio_value
    return result



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
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
