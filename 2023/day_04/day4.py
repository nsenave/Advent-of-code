import os.path
import unittest

def line_split(line: str) :
    card_numbers = line.split(': ')[1]
    winning_numbers, player_numbers = card_numbers.split(' | ')
    res = []
    for numbers in (winning_numbers, player_numbers) :
        numbers_list = []
        for string_number in numbers.split(' ') :
            if string_number != '':
                numbers_list.append(int(string_number))
        res.append(numbers_list)
    return res

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def count_matches(card):
    matches = 0
    for number in card[1] :
        if number in card[0] :
            matches += 1
    return matches

def r1(a) :
    if a is None :
        return None
    result = 0
    for card in a:
        matches = count_matches(card)
        score = int(2**(matches-1))
        #print(score)
        result += score
    return result



def r2(a) :
    if a is None :
        return None
    n = len(a)
    cards_count = [1 for i in range(n)]
    for i in range(n):
        card = a[i]
        copies = cards_count[i]
        matches = count_matches(card)
        for k in range(matches) :
            if i+1+k < n :
                cards_count[i+1+k] += copies
    #print(cards_count)
    return sum(cards_count)



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
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
