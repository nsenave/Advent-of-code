import unittest
import numpy as np

def line_split(line) :
    res = line.split(' ')
    return (res[0], int(res[1]))

def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('example/input.txt')
example2 = parse_input('example/input2.txt')

print("Example input:")
print(example)



def init_canvas(moves) :
    """Init a canvas ensuring enough space to make dots of the row according to moves given.
    Arguments:
        moves: list of moves parsed from input.
    Return:
        - A numpy array containing zeros (integers).
        - The statring coordinates that ensure that moves given will not go out of bounds.
    """
    u,d,l,r = 0,0,0,0
    for move in moves :
        direction = move[0]
        distance = move[1]
        if direction == 'U' :
            u += distance
        elif direction == 'D' :
            d += distance
        elif direction == 'L' :
            l += distance
        elif direction == 'R' :
            r += distance
    return np.zeros((u+d, l+r), dtype=int), (u-1, l-1)

def close_enough(x1,y1,x2,y2) :
    return abs(x1-x2) <= 1 and abs(y1-y2) <= 1

def r1(a) :
    canvas, start = init_canvas(a)
    x1,y1 = start # head coords
    x2,y2 = start # tail coords
    canvas[x2,y2] = 1
    for move in a :
        direction = move[0]
        distance = move[1]
        if direction == 'U' :
            for k in range(distance) :
                x1 -= 1
                if not close_enough(x1,y1,x2,y2) :
                    x2, y2 = x1+1, y1
                    canvas[x2,y2] = 1
        elif direction == 'D' :
            for k in range(distance) :
                x1 += 1
                if not close_enough(x1,y1,x2,y2) :
                    x2, y2 = x1-1, y1
                    canvas[x2,y2] = 1
        elif direction == 'L' :
            for k in range(distance) :
                y1 -= 1
                if not close_enough(x1,y1,x2,y2) :
                    x2, y2 = x1, y1+1
                    canvas[x2,y2] = 1
        elif direction == 'R' :
            for k in range(distance) :
                y1 += 1
                if not close_enough(x1,y1,x2,y2) :
                    x2, y2 = x1, y1-1
                    canvas[x2,y2] = 1
        #print(canvas)
    return np.sum(canvas)



class Dot :
    def __init__(self, x:int, y:int) :
        self.x = x
        self.y = y
    def __init__(self, start: tuple) :
        self.x, self.y = start

def up(dot: Dot) :
    dot.x -= 1
def down(dot: Dot) :
    dot.x += 1
def left(dot: Dot) :
    dot.y -= 1
def right(dot: Dot) :
    dot.y += 1

def propagate(d1: Dot, d2: Dot) :
    """Propagates movement and return a boolean to indicate if propagation continues.
    Arguments:
        d1: a Dot that has moved
        d2: a Dot that has not moved
    Return:
        True if d2 has been moved, (i.e. d1 movement propagated to d2).
    """
    dx = abs(d1.x - d2.x)
    dy = abs(d1.y - d2.y)
    if dx <= 1 and dy <= 1 :
        return False
    else :
        if dx == 1 :
            d2.x = d1.x
        elif dx == 2 :
            d2.x = (d1.x + d2.x) // 2
        if dy == 1 :
            d2.y = d1.y
        elif dy == 2 :
            d2.y = (d1.y + d2.y) // 2
        return True

def print_canvas(canvas, dots) :
    display_canvas = [['.' for k in range(canvas.shape[1])] for i in range(canvas.shape[0])]
    for k in range(len(dots)) :
        dot = dots[k]
        display_canvas[dot.x][dot.y] = 'H' if k==0 else str(k)
    print('\n'.join( list(map(lambda display_line: ' '.join(display_line), display_canvas))) )

def r2(a, debug=False) :
    canvas, start = init_canvas(a)
    dots = [Dot(start) for n in range(10)]
    head = dots[0]
    tail = dots[-1]
    canvas[tail.x, tail.y] = 1
    for move in a :
        if debug : print(move)
        direction = move[0]
        distance = move[1]
        #
        if direction == 'U' :
            move_function = up
        elif direction == 'D' :
            move_function = down
        elif direction == 'L' :
            move_function = left
        elif direction == 'R' :
            move_function = right
        #
        for k in range(distance) :
            d1 = head
            move_function(d1)
            d2 = dots[1]
            n = 1
            while propagate(d1, d2) and n < 10-1 :
                n += 1
                d1, d2 = d2, dots[n]
            canvas[tail.x, tail.y] = 1
        if debug : print_canvas(canvas, dots)
    return np.sum(canvas)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertTrue(close_enough(2,2,1,1))
        self.assertTrue(close_enough(2,1,1,1))
        self.assertFalse(close_enough(2,3,1,1))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example, debug=True)}")
    print(f"Example 2 result: {r2(example2)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
