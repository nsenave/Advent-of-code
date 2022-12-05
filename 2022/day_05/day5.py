import unittest

def parse_crates(crates: str) -> list :
    lines_str = crates.split('\n')
    lines_str.pop()
    n = len(lines_str)
    m = len(lines_str[-1].split(' '))
    res = [[] for k in range(m)]
    for i in range(n) :
        for j in range(m) :
            crate = lines_str[n-1-i][j*4+1]
            if crate != ' ' :
                res[j].append(crate)
    return res

def parse_instructions(instructions: str) -> list :
    res = []
    for instruction in instructions.split('\n') :
        tmp = instruction.split(' ')
        res.append((int(tmp[1]), int(tmp[3]), int(tmp[5])))
    return res

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        crates_str, instructions_str = f.read().split('\n\n')
        return (parse_crates(crates_str), parse_instructions(instructions_str))

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def r1(a) :
    crates, instructions = a
    for instruction in instructions :
        j1, j2 = instruction[1] - 1, instruction[2] - 1
        for k in range(instruction[0]) :
            crates[j2].append(crates[j1].pop())
    #print(crates)
    res = ""
    for crate in crates :
        res += crate.pop()
    return res



def r2(a) :
    crates, instructions = a
    for instruction in instructions :
        j1, j2 = instruction[1] - 1, instruction[2] - 1
        moved = []
        quantity = instruction[0]
        for k in range(quantity) :
            moved.append(crates[j1].pop())
        for k in range(quantity) :
            crates[j2].append(moved[quantity-1-k])
    #print(crates)
    res = ""
    for crate in crates :
        res += crate.pop()
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

    puzzle = parse_input('input.txt')
    example = parse_input('example/input.txt')
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
