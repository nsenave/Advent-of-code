import os.path
import unittest

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(lambda line : line.split('\n'), f.read().split('\n\n')))

example = parse_input('input-example.txt')
puzzle = parse_input('input.txt')

print("Example input:")
print(example)



def is_vertical_symetry(line: str, j_axis: int):
    m = len(line)
    for j in range(0, min(j_axis + 1, m - j_axis - 1)):
        if line[j_axis - j] != line[j_axis + j + 1] :
            return False
    return True

def find_vertical_axis(terrain: list) -> int:
    m = len(terrain[0])
    possible_axis = [j for j in range(m-1)]
    for line in terrain:
        not_axes = []
        for j in possible_axis:
            if not is_vertical_symetry(line, j) :
                not_axes.append(j)
        for j in not_axes:
            possible_axis.remove(j)
    axis_count = len(possible_axis)
    if axis_count > 1:
        raise RuntimeError("Didn't expect there would be sevral mirrors.")
    if axis_count == 1:
        return possible_axis[0]
    return None

def is_horizontal_symetry(terrain: list, i_axis: int, j: int) -> bool:
    n = len(terrain)
    for i in range(0, min(i_axis + 1, n - i_axis - 1)):
        if terrain[i_axis - i][j] != terrain[i_axis + i + 1][j] :
            return False
    return True

def find_horizontal_axis(terrain: list) -> int:
    n, m = len(terrain), len(terrain[0])
    possible_axis = [i for i in range(n-1)]
    for j in range(m):
        not_axes = []
        for i in possible_axis:
            if not is_horizontal_symetry(terrain, i, j) :
                not_axes.append(i)
        for i in not_axes:
            possible_axis.remove(i)
    axis_count = len(possible_axis)
    if axis_count > 1:
        raise RuntimeError("Didn't expect there would be sevral mirrors.")
    if axis_count == 1:
        return possible_axis[0]
    return None

def reflection_number(terrain: list, vertical_axis: int, horizontal_axis: int) -> int:
    if (vertical_axis is not None) and (horizontal_axis is not None):
        raise RuntimeError("Didn't expect to have both a vertical and a vertical mirror.")
    if vertical_axis is not None:
        return vertical_axis + 1
    if horizontal_axis is not None:
        return 100 * (horizontal_axis + 1)
    print("Didn't find a symetry in following terrain:")
    print('\n'.join(terrain))
    raise RuntimeError("Didn't find neither vertical nor horizontal mirror.")

def r1(a) :
    if a is None :
        return None
    res = 0
    for terrain in a:
        vertical_axis = find_vertical_axis(terrain)
        horizontal_axis = find_horizontal_axis(terrain)
        number = reflection_number(terrain, vertical_axis, horizontal_axis)
        #print(number)
        res += number
    return res



def smudge_vertical_symetry(terrain: list, j_axis: int) -> bool:
    """Return true is changing exactly one smudge in the terrain creates a vertical symetry 
    at around j_axis given."""
    n, m = len(terrain), len(terrain[0])
    score = 0
    for line in terrain:
        for j in range(0, min(j_axis + 1, m - j_axis - 1)):
            if line[j_axis - j] != line[j_axis + j + 1] :
                score += 1
                if score > 1:
                    return False
    return True if score == 1 else False

def smudge_horizontal_symetry(terrain: list, i_axis: int) -> bool:
    """Return true is changing exactly one smudge in the terrain creates a horizontal symetry 
    at around i_axis given."""
    n, m = len(terrain), len(terrain[0])
    score = 0
    for j in range(m):
        for i in range(0, min(i_axis + 1, n - i_axis - 1)):
            if terrain[i_axis - i][j] != terrain[i_axis + i + 1][j] :
                score += 1
                if score > 1:
                    return False
    return True if score == 1 else False

def r2(a) :
    if a is None :
        return None
    res = 0
    for terrain in a:
        n, m = len(terrain), len(terrain[0])
        vertical_axis = None
        horizontal_axis = None
        for j_axis in range(m-1):
            if smudge_vertical_symetry(terrain, j_axis):
                vertical_axis = j_axis
                break
        for i_axis in range(n-1):
            if smudge_horizontal_symetry(terrain, i_axis):
                horizontal_axis = i_axis
                break
        res += reflection_number(terrain, vertical_axis, horizontal_axis)
    return res



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
