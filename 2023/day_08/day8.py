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



example_part2 = parse_input('input-example-part-2.txt')

# This would be a way to do it if the input was not so "convenient".
# Idea: state = curent_node x position on the instructions' ribbon.
# There is a finite number of states so the cycle will loop on a repeating sequence.
# Yet, as there is about 1000 nodes and the ribbon length is about 1000, 
# there are a million possible states...
# Using a GPU would maybe make this algorithm work in a reasonable time.
def find_repeating_sequence(nodes: dict, start: str, instructions: str) -> tuple:
    n = len(instructions)
    encountered_states = []
    # Apply the cycle until a repeating sequence is found (i.e. a state occurs for the second time)
    current_node = start
    current_instruction = instructions[0]
    k = 0
    current_state = (start, k)
    while current_state not in encountered_states:
        encountered_states.append((current_node, current_instruction))
        current_node = get_node(nodes, current_node, current_instruction)
        k += 1
        if k == n:
            k = 0
        current_instruction = instructions[k]
        current_state = (current_node, k)
    # Find where are the 'Z' nodes in the repeating sequence
    n_states = len(encountered_states)
    sequence_start = encountered_states.index(current_state)
    sequence_length = n_states - sequence_start
    z_nodes_positions = []
    i = 0
    for state in encountered_states[sequence_start:]:
        node = state[0]
        if node.endswith('Z'):
            z_nodes_positions.append(i)
        i += 1
    print(f"""
          Starting from {start}, repeating sequence from step {sequence_start} of length {sequence_length}
          Start: {encountered_states[sequence_start:min(sequence_start+2, n_states)]}...
          End:   ...{encountered_states[max(0, n_states-2):]}
          (Next state being {current_state})
          Nodes that ends with 'Z' at following positions in the repeating sequence:
          {z_nodes_positions}""")
    if len(z_nodes_positions) == 0:
        print(encountered_states)
        raise RuntimeError("Expecting that each repeating sequence would contain at least one ending 'Z' node.")
    return sequence_start, sequence_length, z_nodes_positions

def find_first_zs(nodes: dict, start: str, instructions: str, z_number=3):
    current_node = start
    steps = 0
    n = len(instructions)
    z_positions = []
    k = 0
    while len(z_positions) < z_number:
        instruction = instructions[k]
        #print(current_node, nodes[current_node], instruction)
        current_node = get_node(nodes, current_node, instruction)
        steps += 1
        if current_node.endswith('Z'):
            z_positions.append(steps)
        k += 1
        if k == n:
            k = 0
    print(f"From {start}: {z_positions}..., diffs = {[z_positions[k+1] - z_positions[k] for k in range(z_number-1)]}...")
    # Input is made so that z nodes are evenly spaced
    return z_positions[0]

def r2(a) :
    if a is None :
        return None
    instructions, nodes = a
    first_z_positions = []
    for node in nodes:
        if node.endswith('A'):
            first_z_positions.append(find_first_zs(nodes, node, instructions))
    return lcm(first_z_positions)

def gcd(n, m):
    if m == 0:
        return n
    return gcd(m, n % m)

def lcm(integers: list):
    res = 1
    for i in integers:
        res = res * i // gcd(res, i)
    return res



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
    print(f"Example result:    {r2(example_part2)}")
    print(f"Puzzle answer:     {r2(puzzle)}")
