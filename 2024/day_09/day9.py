import os.path
import unittest
import time

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return f.read()



def decompress(compressed: str, id=0) -> list:
    res = []
    for i in range(0, len(compressed) - 1, 2):
        file_size = int(compressed[i])
        empty_size = int(compressed[i + 1])
        for _ in range(file_size):
            res.append(str(id))
        for _ in range(empty_size):
            res.append('.')
        id += 1
    if len(compressed) % 2 == 1:
        res += str(id) * int(compressed[-1])
    return res

def get_last(blocks: list, length: int):
    i = length - 1
    while i >= 0 and blocks[i] == '.':
        i -= 1
    return blocks[i], i

def get_first_empty(block: list):
    i = 0
    while block[i] != '.':
        i += 1
    return i

def rearrange_blocks(blocks: list):
    length = len(blocks)
    block, end_index = get_last(blocks, length)
    start_index = get_first_empty(blocks)
    while start_index < end_index:
        blocks[end_index] = '.'
        blocks[start_index] = block
        block, end_index = get_last(blocks, length)
        start_index = get_first_empty(blocks)

def rearrange(decompressed: str) -> str:
    blocks = list(decompressed)
    rearrange_blocks(blocks)
    return ''.join(blocks)

def compute_checksum_rearranged(rearranged: str, position=0):
    res = 0
    i = 0
    while rearranged[i] != '.':
        res += position * int(rearranged[i])
        i += 1
        position += 1
    return res

def get_first_group(blocks: list):
    return blocks.pop(0), blocks.pop(0)

def get_last_file_size(blocks: list):
    blocks.pop()
    return int(blocks.pop())

def insert_file(file_id: int, file_size: int, blocks: list):
    remplacements = 0
    i = 0
    size = len(blocks)
    while remplacements < file_size:
        if i >= size:
            blocks.append(file_id)
            remplacements += 1
        elif blocks[i] == '.':
            blocks[i] = file_id
            remplacements += 1
        i += 1

def compute_checksum_compressed(compressed: str, debug=False):
    blocks = list(compressed + '0')
    checksum = 0
    position = 0
    id = 0
    current_section = []
    empty_space = 0
    file_end_id = len(compressed) // 2
    steps = 0
    while blocks:
        if debug:
            print(f"Compressed blocks: {blocks}")
        file_end_size = get_last_file_size(blocks)
        if debug:
            print(f"Compressed blocks: {blocks}")
            print(f"About to insert file '{file_end_id}' of size {file_end_size}")
        while blocks and empty_space < file_end_size:
            file_start, empty_start = get_first_group(blocks)
            decompressed = decompress(file_start + empty_start, id)
            if debug:
                print(f"New decompressed block: {decompressed}")
            current_section.extend(decompressed)
            id += 1
            empty_space += int(empty_start)
        if debug:
            print(f"Compressed blocks: {blocks}")
        if debug:
            print(f"Current section: {current_section} (empty space = {empty_space})")
        insert_file(str(file_end_id), file_end_size, current_section)
        empty_space -= file_end_size
        if debug:
            print(f"After insertion: {current_section} (empty space = {empty_space})")
        file_end_id -= 1
        #
        i = 0
        while current_section and current_section[i] != '.':
            checksum += position * int(current_section.pop(0))
            position += 1
        if debug:
            print(f"After checksmuing: {current_section} (empty space = {empty_space})")
            print("---")
        steps += 1
    print(f"Final state: {current_section}")
    print(f"Number of steps: {steps}")
    return checksum

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    print(f"Length of compressed input: {len(puzzle_input)}")
    if debug:
        print(f"Result on decompressed data: {compute_checksum_rearranged(rearrange(''.join(decompress(puzzle_input))))}")
    return compute_checksum_compressed(puzzle_input, debug)
#90192861055
#9509965953053



def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    res = 0
    for x in puzzle_input :
        pass
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_decompress(self):
        self.assertEqual("0..111....22222", decompress("12345"))
        self.assertEqual("000000000111111111222222222", decompress("90909"))
        self.assertEqual("00...111...2...333.44.5555.6666.777.888899", decompress("2333133121414131402"))
    
    def test_rearrange(self):
        self.assertEqual("022111222......", rearrange("0..111....22222"))
        self.assertEqual("0099811188827773336446555566..............", rearrange("00...111...2...333.44.5555.6666.777.888899"))
        self.assertEqual("02111......", rearrange("0..111....2"))
        self.assertEqual("03211......", rearrange("0..112....3"))
    
    def test_insert(self):
        blocks = ['0', '.', '.', '1', '1', '1', '.', '.', '.', '.']
        expected = ['0', '2', '.', '1', '1', '1', '.', '.', '.', '.']
        insert_file('2', 1, blocks)
        self.assertEqual(expected, blocks)
    
    def test_compute_checksum_compressed(self):
        self.assertEqual(2+4+3+4+5+12+14+16, compute_checksum_compressed("12345"))
        self.assertEqual(2+2+3+4, compute_checksum_compressed("12341"))
        self.assertEqual(6, compute_checksum_compressed("123"))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')
    assert puzzle[:3] == "252"
    assert puzzle[-3:] == "332"

    print("--- Part One ---")
    t0 = time.time()
    print(f"Example result: {r1(example, True)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    t1 = time.time()
    print(f"Part one computed in {t1 - t0} seconds.")

    print("--- Part Two ---")
    t0 = time.time()
    print(f"Example result: {r2(example, True)}")
    #print(f"Puzzle answer:  {r2(puzzle)}")
    t1 = time.time()
    print(f"Part two computed in {t1 - t0} seconds.")
