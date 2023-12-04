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
            if current_number != '' and is_symbol_around(a, i, j0, j-1) :
                result += int(current_number)
                #print(current_number)
            j += 1
    return result



def scan_part_number_right(row:np.array, j_start:int, j_gear:int) -> str:
    res = ''
    j = j_start
    while j <= j_gear or is_number(row[j]) :
        res += row[j]
        j += 1
    return res

def scan_part_number_left(row:np.array, j_start:int, j_gear:int) -> str:
    res = ''
    j = j_start
    while j >= j_gear or is_number(row[j]) :
        res = row[j] + res
        j -= 1
    return res

def find_part_numbers(scaned_string: str) -> set:
    cleaned_string = ''
    for c in scaned_string:
        cleaned_string += c if is_number(c) else ' '
    res = cleaned_string.split(' ')
    while '' in res:
        res.remove('')
    return list(map(int, res))

def gear_ratio(a: np.array, i_gear: int, j_gear: int) -> int:
    part_numbers = []
    # Above row
    part_numbers += find_part_numbers(
        scan_part_number_left(a[i_gear-1,:], j_gear-1, j_gear) + scan_part_number_right(a[i_gear-1,:], j_gear, j_gear))
    # Left from gear
    part_numbers += find_part_numbers(
        scan_part_number_left(a[i_gear,:], j_gear-1, j_gear))
    # Right from gear
    part_numbers += find_part_numbers(
        scan_part_number_right(a[i_gear,:], j_gear+1, j_gear))
    # Below row
    part_numbers += find_part_numbers(
        scan_part_number_left(a[i_gear+1,:], j_gear-1, j_gear) + scan_part_number_right(a[i_gear+1,:], j_gear, j_gear))
    #print(part_numbers)
    if len(part_numbers) != 2 :
        return None
    return part_numbers[0] * part_numbers[1]

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
        self.assertEqual('.755', scan_part_number_right(np.array(['.', '.', '.', '.', '.', '.', '.', '7', '5', '5', '.', '.']), 6, 6))
        self.assertEqual('598', scan_part_number_right(np.array(['.', '.', '6', '6', '4', '.', '5', '9', '8', '.', '.', '.']), 6, 6))
        self.assertEqual('', scan_part_number_left(np.array(['.', '.', '6', '6', '4', '.', '5', '9', '8', '.', '.', '.']), 5, 6))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
