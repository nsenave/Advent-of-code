import os.path
import unittest
from typing import List, Dict



COLORS = ['r', 'g', 'b']

class Game:
    def __init__(self, id: int, sets: List[Dict]):
        self.id = id
        self.sets = sets
    def __str__(self):
        return f"Game {self.id}: {self.sets}"


def line_split(line: str) :
    game_string, sets_string = line.split(': ')
    game_id = int(game_string[5:]) # 'Game <id>'
    game_sets = []
    for string_set in sets_string.split('; ') :
        game_set = {}
        for color in COLORS:
            game_set[color] = 0
        for string_entry in string_set.split(', ') :
            number_string, color_string = string_entry.split(' ')
            game_set[color_string[0]] = int(number_string)
        game_sets.append(game_set)
    return Game(game_id, game_sets)

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
for game in example:
    print(game)



def is_valid_game(game: Game, max_red: int, max_green: int, max_blue: int) -> bool:
    for game_set in game.sets:
        if game_set['r'] > max_red:
            return False
        if game_set['g'] > max_green:
            return False
        if game_set['b'] > max_blue:
            return False
    return True

def r1(a) :
    if a is None :
        return None
    result = 0
    for game in a:
        if is_valid_game(game, 12, 13, 14):
            result += game.id
    return result



def r2(a) :
    if a is None :
        return None
    result = 0
    for game in a:
        color_counts = {}
        for color in COLORS:
            color_counts[color] = []
        for color in COLORS:
            for game_set in game.sets:
                color_counts[color].append(game_set[color])
        result += max(color_counts['r']) * max(color_counts['g']) * max(color_counts['b'])
    return result



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
