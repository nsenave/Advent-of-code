import os.path
import unittest
import time
from functools import cache

def line_split(line: str) :
    parts = line.split(': ')
    return parts[0], parts[1].split(' ')

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))



devices = {}
out_paths = set()

def cut(path: str):
    return [path[i : i+3] for i in range(0, len(path), 3)]

@cache
def walk(label, path):
    global devices, out_paths
    for output in devices[label]:
        if output == 'out':
            out_paths.add(path)
            continue
        assert output not in cut(path), f"Infinite loop! {output} in {path}"
        walk(output, output + path)

def r1(puzzle_input, debug=False) :
    global devices, out_paths
    devices = {}
    out_paths = set()
    if puzzle_input is None:
        return None
    for x in puzzle_input :
        device, outputs = x
        devices[device] = outputs
    if debug:
        print(devices)
    walk('you', '')
    return len(out_paths)



# doesn't work wit personal input
@cache
def walk2(label, path):
    global devices, out_paths
    for output in devices[label]:
        if output == 'out':
            cutted = cut(path)
            if (('dac' in cutted) and ('fft' in cutted)):
                out_paths.add(path)
            continue
        assert output not in cut(path), f"Infinite loop! {output} in {path}"
        walk2(output, output + path)

def r2(puzzle_input, debug=False) :
    global devices, out_paths
    devices = {}
    out_paths = set()
    if puzzle_input is None:
        return None
    for x in puzzle_input :
        device, outputs = x
        devices[device] = outputs
    walk2('svr', '')
    if debug:
        print(out_paths)
    return len(out_paths)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        cutted = cut('gggfffhubdddcccfftaaa')
        self.assertEqual(False, ('dac' in cutted) and ('fft' in cutted))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')

    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    walk.cache_clear()
    devices = {}
    out_paths = set()
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    example2 = parse_input('input-example2.txt')
    print("Example input:")
    print(example2)

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example2, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
