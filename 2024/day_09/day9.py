import os.path
import unittest
import time

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        print(f"File {file_path} not found.")
        return None
    with open(file_path, 'r') as f :
        return f.read()


# --- Part One ---

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

# Naive approach
# (kept as a control on the example input)

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

def rearrange(blocks: list) -> list:
    """Rearrange the elements of the given list."""
    length = len(blocks)
    block, end_index = get_last(blocks, length)
    start_index = get_first_empty(blocks)
    while start_index < end_index:
        blocks[end_index] = '.'
        blocks[start_index] = block
        block, end_index = get_last(blocks, length)
        start_index = get_first_empty(blocks)
    return blocks

def compute_checksum(blocks: list, position=0):
    res = 0
    for i in range(len(blocks)):
        if blocks[i] != '.':
            res += position * int(blocks[i])
            position += 1
    return res

def compact_checksum_naive(compressed: str) -> int:
    """Naive approch were the input is fully decompressed before computing checksum."""
    return compute_checksum(rearrange(decompress(compressed)))

# More efficient approach by computing the checksum by small pieces

def pop_first_group(blocks: list):
    return blocks.pop(0), blocks.pop(0)

def pop_last_file_size(blocks: list):
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

def compact_checksum(compressed: str, debug=False):
    blocks = list(compressed + '0')
    checksum = 0
    position = 0
    id = 0
    current_section = []
    empty_space = 0
    file_end_id = len(compressed) // 2
    if debug:
        print("--- Start compacting and calculating checksum ---")
    while blocks:
        if debug:
            print(f"Compressed blocks: {blocks}")
        file_end_size = pop_last_file_size(blocks)
        if debug:
            print(f"About to insert file '{file_end_id}' of size {file_end_size}")
        while blocks and empty_space < file_end_size:
            file_start, empty_start = pop_first_group(blocks)
            decompressed = decompress(file_start + empty_start, id)
            if debug:
                print(f"Decompressed block {[file_start, empty_start]} to : {decompressed}")
            current_section.extend(decompressed)
            id += 1
            empty_space += int(empty_start)
        if debug:
            print(f"Current section: {current_section} (empty space = {empty_space})")
        insert_file(str(file_end_id), file_end_size, current_section)
        empty_space -= file_end_size # (can eventually be negative on last iteration but it's ok)
        if debug:
            print(f"After insertion: {current_section} (empty space = {empty_space})")
        file_end_id -= 1
        # Compute checksum on current section while freeing up memory space
        i = 0
        while current_section and current_section[i] != '.':
            checksum += position * int(current_section.pop(0))
            position += 1
        if debug:
            print(f"After checksmuing: {current_section} (empty space = {empty_space})")
            print("")
    return checksum

def r1(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    print(f"Length of compressed input: {len(puzzle_input)}")
    res = compact_checksum(puzzle_input, debug)
    if debug:
        print(f"Result on decompressed data: {compact_checksum_naive(puzzle_input)}")
    return res



# --- Part Two ---

def insert_at(index: int, elements: list, some_list: list) -> list:
    some_list[index:index] = elements
    return some_list

def decompress_with_register(compressed: str, ids_register) -> list:
    res = []
    for i in range(0, len(compressed) - 1, 2):
        id = ids_register[i // 2]
        file_size = int(compressed[i])
        empty_size = int(compressed[i + 1])
        for _ in range(file_size):
            res.append(str(id))
        for _ in range(empty_size):
            res.append('.')
    if len(compressed) % 2 == 1:
        res += str(id) * int(compressed[-1])
    return res

def defragment(disk_map: str, debug=False):
    blocks = list(disk_map + '0')
    file_end_id = len(disk_map) // 2
    ids_register = [id for id in range(file_end_id + 1)]
    if debug:
        print("--- Start defragmenting ---")
    for id in reversed(range(1, file_end_id + 1)):
        if debug:
            print(f"Register: {ids_register}")
            print(f"Compressed blocks: {blocks}")
        position = ids_register.index(id) * 2
        size = int(blocks[position])
        if debug:
            print(f"About to insert file '{id}' of size {blocks[position]}")
        i = 0
        while size > int(blocks[i+1]) and i < position:
            i += 2
        if debug:
            print(f"File '{id}' can be inserted in empty space at {i}")
        if i != position:
            file_empty_size = int(blocks[i+1])
            blocks[i+1] = '0'
            blocks.pop(position)
            blocks.pop(position)
            insert_at(i+2, [str(size), str(file_empty_size - size)], blocks)
            blocks[position + 1] = str(int(blocks[position + 1]) + size)
            ids_register.remove(id)
            ids_register.insert(i // 2 + 1, id)
        if debug:
            print(f"Disk after '{9}': {''.join(decompress_with_register()}")
    if debug:
        print(f"Final register: {ids_register}")
        print(f"Final disk map: {blocks}")
    return blocks, ids_register

def compute_checksum_compressed(blocks: list, ids_register: list) -> int:
    res = 0
    position = 0
    for i in range(len(ids_register)):
        id = ids_register[i]
        size, empty = int(blocks[i*2]), int(blocks[i*2 + 1])
        for _ in range(size):
            res += position * id
            position += 1
        for _ in range(empty):
            position += 1
    return res

def defragment_checksum(map_disk: str, debug=False):
    defragmented, ids_register = defragment(map_disk, debug)
    return compute_checksum_compressed(defragmented, ids_register)

def r2(puzzle_input, debug=False) :
    if puzzle_input is None:
        return None
    return defragment_checksum(puzzle_input, debug)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_decompress(self):
        self.assertEqual(list("0..111....22222"), decompress("12345"))
        self.assertEqual(list("000000000111111111222222222"), decompress("90909"))
        self.assertEqual(list("00...111...2...333.44.5555.6666.777.888899"), decompress("2333133121414131402"))
    
    def test_rearrange(self):
        self.assertEqual(list("022111222......"), rearrange(list("0..111....22222")))
        self.assertEqual(list("0099811188827773336446555566.............."), rearrange(list("00...111...2...333.44.5555.6666.777.888899")))
        self.assertEqual(list("02111......"), rearrange(list("0..111....2")))
        self.assertEqual(list("03211......"), rearrange(list("0..112....3")))
    
    def test_insert(self):
        blocks = ['0', '.', '.', '1', '1', '1', '.', '.', '.', '.']
        expected = ['0', '2', '.', '1', '1', '1', '.', '.', '.', '.']
        insert_file('2', 1, blocks)
        self.assertEqual(expected, blocks)
    
    def test_compact_checksum(self):
        self.assertEqual(2+4+3+4+5+12+14+16, compact_checksum("12345"))
        self.assertEqual(2+2+3+4, compact_checksum("12341"))
        self.assertEqual(6, compact_checksum("123"))
    
    def test_insert_at(self):
        some_list = [1,2,5]
        expected = [1,2,3,4,5]
        insert_at(2, [3,4], some_list)
        self.assertEqual(expected, some_list)

    def test_defragment_checksum(self):
        self.assertEqual(10+6+7+8, defragment_checksum("54321"))

if __name__ == '__main__':
    unittest.main(exit=False)

    example = parse_input('input-example.txt')
    print("Example input:")
    print(example)

    puzzle = parse_input('input.txt')

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
