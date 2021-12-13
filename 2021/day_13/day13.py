import unittest
import numpy as np

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        raw_dots, raw_instructions = f.read().split('\n\n')
        dots = list(map(lambda x: tuple(map(int, x.split(','))), raw_dots.split('\n')))
        instructions = list(map(lambda x: (x[11], int(x[13:])), raw_instructions.split('\n')))
    return dots, instructions

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')

print("Example input:")
print(example)



def create_paper(dots) :
    n = max(map(lambda x: x[0], dots)) + 1
    m = max(map(lambda x: x[1], dots)) + 1
    res = np.zeros((m,n), dtype=int)
    for dot in dots :
        x,y = dot
        res[y,x] = 1
    return res

def fold_middle(paper, instruction) :
    """folds in the middle if number of rows/columns is pair 
    (not what is asked)"""
    m,n = paper.shape
    direction, number = instruction
    if direction == 'y' :
        assert number == m//2
        res = np.zeros((number,n), dtype=int)
        for x in range(n) :
            for y in range(number) :
                res[y,x] = max(paper[y,x], paper[m-1-y,x])
    elif direction == 'x' :
        assert number == n//2
        res = np.zeros((m,number), dtype=int)
        for y in range(m) :
            for x in range(number) :
                res[y,x] = max(paper[y,x], paper[y,n-1-x])
    return res

def fold(paper, instruction) :
    m,n = paper.shape
    direction, number = instruction
    if direction == 'y' :  
        assert number >= m//2
        res = paper[:number,:]
        for x in range(n) :
            for y in range(1, m - number) :
                res[number-y,x] = max(paper[number-y,x], paper[number+y,x])
    elif direction == 'x' :
        assert number >= n//2
        res = paper[:,:number]
        for y in range(m) :
            for x in range(1, n - number) :
                res[y,number-x] = max(paper[y,number-x], paper[y,number+x])
    return res

def r1(a) :
    dots, instructions = a
    paper = create_paper(dots)
    folded = fold(paper, instructions[0])
    return sum(map(sum,folded))

def r2(a) :
    dots, instructions = a
    paper = create_paper(dots)
    for instruction in instructions :
        paper = fold(paper, instruction)
    return paper

def print_paper(paper) :
    m,n = paper.shape
    text = ""
    for y in range(m) :
        for x in range(n) :
            if x%(n//8) == 0 :
                text += '  '
            if paper[y,x] == 0 :
                text += ' '
            else :
                text += '#'
        text += '\n'
    print(text)



if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: \n{r2(example)}")
    print("Puzzle answer: ")
    print_paper(r2(puzzle))
