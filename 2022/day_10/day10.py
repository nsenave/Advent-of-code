import unittest

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return f.read().split('\n')

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input (10 firsts):")
print(example[:10])



class CPU :
    def __init__(self) :
        self.cycle = 0
        self.register = 1
    def noop(self) :
        return self.increment()
    def increment(self) :
        self.cycle += 1
        return 0 if self.cycle % 40 != 20 else self.signal_strength()
    def add_value(self, value:int) :
        res = 0
        res += self.increment()
        res += self.increment()
        self.register += value
        return res
    def signal_strength(self) :
        return self.cycle * self.register

def r1(a) :
    cpu = CPU()
    res = 0
    for command in a :
        if command == "noop" :
            res += cpu.noop()
        else :
            value = int(command.split(' ')[1])
            res += cpu.add_value(value)
    return res



class CRT :
    lit_char = '#' # '█'
    dark_char = '.' # ' '
    def __init__(self, wide:int, row:int) :
        self.wide = wide
        self.row = row
        self.current_display = []
    def lit(self) :
        self.current_display.append(1)
    def dark(self) :
        self.current_display.append(0)
    def __str__(self) :
        res = []
        for i in range(self.row) :
            p1 = i * self.wide
            p2 = p1 + self.wide
            res.append(''.join(map(lambda pixel: CRT.lit_char if pixel==1 else CRT.dark_char, self.current_display[p1:p2]))) 
        return '\n'.join(res)
    
class CPU_2 :
    def __init__(self) :
        self.cycle = 0
        self.register = 1
        self.crt = CRT(40, 6)
    def noop(self) :
        self.increment()
    def increment(self) :
        sprite_position = self.register-1
        if sprite_position <= self.cycle%40 < sprite_position+3 :
            self.crt.lit()
        else :
            self.crt.dark()
        self.cycle += 1
    def add_value(self, value:int) :
        self.increment()
        self.increment()
        self.register += value

def r2(a) :
    cpu = CPU_2()
    res = 0
    for command in a :
        if command == "noop" :
            cpu.noop()
        else :
            value = int(command.split(' ')[1])
            cpu.add_value(value)
    print(cpu.crt.current_display[:40])
    return cpu.crt



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
    print(f"Example result:\n{r2(example)}")
    print(f"Puzzle answer:\n{r2(puzzle)}")
