import unittest

def line_split(line) :
    return line.split('-')

with open('input.txt', 'r') as f :
    puzzle = list(map(line_split, f.read().split('\n')))

with open('example/input.txt', 'r') as f :
    example = list(map(line_split, f.read().split('\n')))

print("Example input:")
print(example)



def direct_links(links) :
    res = {}
    for link in links :
        a,b = link
        if a in res :
            res[a].add(b)
        else :
            res[a] = set([b])
        if b in res :
            res[b].add(a)
        else :
            res[b] = set([a])
    return res

print(direct_links(example))

def is_small(cave:str) -> bool :
    return cave == cave.lower()

def explore(caves_map, current_path) :
    current_cave = current_path[-1]
    for cave in caves_map[current_cave] :
        if cave == 'end' :
            yield current_path + [cave]
        else :
            if not (is_small(cave) and (cave in current_path)) :
                for path in explore(caves_map, current_path + [cave]) :
                    yield path


def r1(a) :
    caves_map = direct_links(a)
    return len(list(explore(caves_map, ['start'])))




def explore2(caves_map, current_path, specific_small) :
    current_cave = current_path[-1]
    for cave in caves_map[current_cave] :
        if cave == 'end' :
            yield current_path + [cave]
        else :
            keep_going = True
            if is_small(cave) :
                visits = current_path.count(cave)
                if cave != specific_small :
                    if visits > 0 :
                        keep_going = False
                else :
                    if visits > 1 :
                        keep_going = False
            if keep_going :
                for path in explore2(caves_map, current_path + [cave], specific_small) :
                    yield path

def r2(a) :
    caves_map = direct_links(a)
    small_caves = [cave for cave in caves_map if is_small(cave) and cave not in ('start', 'end')]
    print(small_caves)
    hash_table = []
    res = 0
    for small_cave in small_caves :
        print(small_cave)
        for path in explore2(caves_map, ['start'], small_cave) :
            h = hash(''.join(path))
            if h not in hash_table :
                hash_table.append(h)
                res += 1
    return res



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_small(self):
        self.assertTrue(is_small('b'))
        self.assertFalse(is_small('A'))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
