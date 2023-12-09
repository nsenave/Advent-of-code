import os.path
import unittest

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        instructions, raw_nodes = f.read().split('\n\n')
        nodes = dict()
        for line in raw_nodes.split('\n'):
            key_node, node_values = line.split(' = ')
            nodes[key_node] = (node_values[1:4], node_values[6:9])
        return instructions, nodes

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')
example2 = parse_input('input-example2.txt')

print("Example input:")
print(example)

print("Example 2 input:")
print(example2)



def get_node(nodes: dict, node: str, instruction: str) -> str:
    index = 0 if instruction == 'L' else 1
    return nodes[node][index]

def r1(a) :
    if a is None :
        return None
    instructions, nodes = a
    current_node = 'AAA'
    steps = 0
    n = len(instructions)
    k = 0
    while True:
        instruction = instructions[k]
        current_node = get_node(nodes, current_node, instruction)
        steps += 1
        if current_node == 'ZZZ':
            return steps
        k += 1
        if k == n:
            k = 0



def r2(a) :
    if a is None :
        return None
    return None



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result:    {r1(example)}")
    print(f"Example 2  result: {r1(example2)}")
    print(f"Puzzle answer:     {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result:    {r2(example)}")
    # print(f"Puzzle answer:     {r2(puzzle)}")
