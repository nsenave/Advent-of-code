import unittest



class Folder(dict) :
    def __init__(self, parent_folder) :
        dict.__init__(self)
        self.parent = parent_folder
        self.files = [] # list of integers
        self.size = 0
    
    def compute_size(self) :
        self.size = sum(self.files)
        for name in self :
            subfolder = self[name]
            self.size += subfolder.compute_size()

"""
class File :
    def __init__(self, size) :
        self.size = size
"""

root = Folder(None)
current_folder = root
flat_list = []

def parse_line(line) :
    global root, current_folder
    command = line.split(' ')
    if command[0] == '$' :
        if command[1] == 'cd' :
            if command[2] != ".." :
                name = command[2]
                if name == '/' :
                    current_folder = root
                else :
                    if name in current_folder :
                        current_folder = current_folder[name]
                    else :
                        new_folder = Folder(current_folder)
                        current_folder[name] = new_folder
                        current_folder = new_folder
                        flat_list.append(new_folder)
            else :
                current_folder = current_folder.parent
    else :
        if command[0] == "dir" :
            name = command[1]
            if name not in current_folder :
                new_folder = Folder(current_folder)
                current_folder[name] = new_folder
                flat_list.append(new_folder)
        else :
            file_size = int(command[0])
            current_folder.files.append(file_size)



def parse_input(file_path:str) :
    with open(file_path, 'r') as f :
        for line_str in f.read().split('\n') :
            parse_line(line_str)

parse_input('input.txt')
#parse_input('example/input.txt')

#puzzle = parse_input('input.txt')
#example = parse_input('example/input.txt')

root.compute_size()
print(root.size)



def r1(a: Folder) :
    res = 0
    for folder in flat_list :
        if folder.size <= 100000 :
            res += folder.size
    return res



def r2(a: Folder) :
    total_size = 70000000
    required_space = 30000000
    disired_space = total_size - required_space
    occupied_space = a.size
    candidates = []
    for folder in flat_list :
        if occupied_space - folder.size <= disired_space :
            candidates.append(folder.size)
    print(candidates)
    return min(candidates)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Result: {r1(root)}")
    # print(f"Example result: {r1(example)}")
    # print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Result: {r2(root)}")
    # print(f"Example result: {r2(example)}")
    # print(f"Puzzle answer:  {r2(puzzle)}")
