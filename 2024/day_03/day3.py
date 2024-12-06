import os.path
import re
import unittest

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return f.read()

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')
example2 = parse_input('input-example2.txt')

print("Example input:")
print(example)



def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, puzzle_input)
    if debug :
        print(matches)
    for t in matches:
        n1, n2 = int(t[0]), int(t[1])
        res += n1 * n2
    return res



def scan_text(text: str, matches: list, i=0, do=True, debug=False):
    length  = len(text)
    text = text.replace("a", "")
    text = text.replace("don't", "da")
    if debug :
        print(text)
    else :
        print(text[-100:])
    while i < length - 4 :
        if text[i:i+4] == "do()" :
            do = True
            i += 4
            continue
        if text[i:i+4] == "da()" :
            do = False
            i += 4
            continue
        if text[i:i+4] == "mul(" and do:
            i += 4
            n1 = ""
            while i < length and text[i].isdigit() :
                n1 += text[i]
                i += 1
            if i == length:
                return
            if text[i] != "," :
                continue
            i += 1
            n2 = ""
            while i < length and text[i].isdigit():
                n2 += text[i]
                i += 1
            if i < length and text[i] != ")" :
                continue
            matches.append((int(n1), int(n2)))
        i += 1

def r2(puzzle_input: str, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    matches = []
    scan_text(puzzle_input, matches, debug=debug)
    if debug :
        print(matches)
    else :
        print(matches[:10])
        print(matches[-10:])
    for n1, n2 in matches:
        res += n1 * n2
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
    print(f"Example result: {r2(example2, True)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
