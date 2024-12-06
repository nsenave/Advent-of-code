import os.path
import unittest

def line_split(line: str) :
    return line

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



class Canvas:
    def __init__(self, content: list):
        self.content = content
        self.x_length = len(content)
        self.y_length = len(content[0])
    def get(self, i: int, j: int) -> str:
        if i < 0 or j < 0 or i >= self.x_length or j >= self.y_length:
            return ""
        return self.content[i][j]

def horizontal_search(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "X" \
        and canvas.get(i, j+1) == "M" \
        and canvas.get(i, j+2) == "A" \
        and canvas.get(i, j+3) == "S"
def horizontall_search_bacwards(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "S" \
        and canvas.get(i, j+1) == "A" \
        and canvas.get(i, j+2) == "M" \
        and canvas.get(i, j+3) == "X"

def vertical_search(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "X" \
        and canvas.get(i+1, j) == "M" \
        and canvas.get(i+2, j) == "A" \
        and canvas.get(i+3, j) == "S"
def vertical_search_bacwards(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "S" \
        and canvas.get(i+1, j) == "A" \
        and canvas.get(i+2, j) == "M" \
        and canvas.get(i+3, j) == "X"

def diagonal_search(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "X" \
        and canvas.get(i+1, j+1) == "M" \
        and canvas.get(i+2, j+2) == "A" \
        and canvas.get(i+3, j+3) == "S"
def diagonal_search_bacwards(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "S" \
        and canvas.get(i+1, j+1) == "A" \
        and canvas.get(i+2, j+2) == "M" \
        and canvas.get(i+3, j+3) == "X"

def antidiagonal_search(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "X" \
        and canvas.get(i+1, j-1) == "M" \
        and canvas.get(i+2, j-2) == "A" \
        and canvas.get(i+3, j-3) == "S"
def antidiagonal_search_bacwards(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "S" \
        and canvas.get(i+1, j-1) == "A" \
        and canvas.get(i+2, j-2) == "M" \
        and canvas.get(i+3, j-3) == "X"

SEARCH_FUNCTIONS = [horizontal_search, horizontall_search_bacwards, \
                    vertical_search, vertical_search_bacwards, \
                    diagonal_search, diagonal_search_bacwards, \
                    antidiagonal_search, antidiagonal_search_bacwards]

def r1(puzzle_input: list, debug=False) :
    if puzzle_input is None:
        return None
    canvas = Canvas(puzzle_input)
    res = 0
    print(canvas.x_length)
    print(canvas.y_length)
    for i in range(canvas.x_length) :
        for j in range(canvas.y_length) :
            for search_function in SEARCH_FUNCTIONS:
                is_xmas = search_function(canvas, i, j)
                res += is_xmas
    return res



def diagonal_search2(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i+1, j+1) == "M" \
        and canvas.get(i+2, j+2) == "A" \
        and canvas.get(i+3, j+3) == "S"
def diagonal_search_bacwards2(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "S" \
        and canvas.get(i+1, j+1) == "A" \
        and canvas.get(i+2, j+2) == "M"

def antidiagonal_search2(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i+1, j-1) == "M" \
        and canvas.get(i+2, j-2) == "A" \
        and canvas.get(i+3, j-3) == "S"
def antidiagonal_search_bacwards2(canvas: Canvas, i: int, j: int) -> bool:
    return canvas.get(i, j) == "S" \
        and canvas.get(i+1, j-1) == "A" \
        and canvas.get(i+2, j-2) == "M"

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    canvas = Canvas(puzzle_input)
    res = 0
    print(canvas.x_length)
    print(canvas.y_length)
    for i in range(canvas.x_length) :
        for j in range(canvas.y_length) :
            is_xmas = (diagonal_search2(canvas, i-1, j-1) or diagonal_search_bacwards2(canvas, i, j)) \
                and (antidiagonal_search2(canvas, i-1, j+3) or antidiagonal_search_bacwards2(canvas, i, j+2))
            res += is_xmas
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
