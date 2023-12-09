import os.path
import unittest
from collections import Counter
from functools import cmp_to_key

class Hand:
    def __init__(self, cards:str):
        self.cards = cards
        self.strength = None
        self.strength_with_joker = None
    def get_strength(self, joker=False):
        if not joker :
            if self.strength is None:
                self.strength = strength(self.cards, False)
            return self.strength
        if joker :
            if self.strength_with_joker is None:
                self.strength_with_joker = strength(self.cards, True)
            return self.strength_with_joker
    def __str__(self) -> str:
        return f"Hand({self.cards})"
    def __repr__(self) -> str:
        return str(self)

class Turn:
    def __init__(self, hand:str, bid: int):
        self.hand = hand
        self.bid = bid
    def __str__(self) -> str:
        return f"Turn({self.hand}, {self.bid})"
    def __repr__(self) -> str:
        return str(self)

def line_split(line: str) :
    string_hand, string_bin = line.split()
    return Turn(Hand(string_hand), int(string_bin))

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return list(map(line_split, f.read().split('\n')))

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



CARD_VALUES = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

def card_value(card:str, joker=False) -> int:
    if card == 'J'and joker:
        return 1
    return CARD_VALUES[card]

def strength(cards: str, joker=False) -> int:
    if not joker:
        counts = Counter(cards)
        jokers = 0
    else: 
        if cards == 'JJJJJ':
            return 50
        cards_without_jokers = cards.replace('J', '')
        counts = Counter(cards_without_jokers)
        jokers = len(cards) - len(cards_without_jokers)
    max_of_a_kind = max(counts.values())
    if max_of_a_kind == 5:
        return 50
    if max_of_a_kind == 4:
        return 40 + 10*jokers
    if max_of_a_kind == 3:
        if jokers > 0:
            return 30 + 10*jokers
        if 2 in counts.values():
            return 35
        return 30
    if max_of_a_kind == 2:
        if jokers >= 2:
            return 20 + 10*jokers
        another_pair = list(counts.values()).count(2) == 2
        if another_pair:
            if jokers == 1:
                return 35
        if jokers == 1:
            return 30
        if another_pair:
            return 25
        return 20
    if max_of_a_kind == 1:
        if jokers > 0:
            return 10 + 10*jokers
    return 15

def lower_than(hand1: Hand, hand2: Hand, joker=False) -> bool:
    """Return true if the first hand has a lower value."""
    strength1 = hand1.get_strength(joker)
    strength2 = hand2.get_strength(joker)
    if strength1 != strength2:
        return strength1 < strength2
    for card1, card2 in zip(hand1.cards, hand2.cards):
        value1 = card_value(card1, joker)
        value2 = card_value(card2, joker)
        if value1 != value2:
            return value1 < value2
    raise ValueError("Didn't expect to have identical cards.")

def compare(turn1: Turn, turn2: Turn, joker=False) -> bool:
    return -1 if lower_than(turn1.hand, turn2.hand, joker) else 1

def compute_winnings(turns):
    result = 0
    n = len(turns)
    for k in range(n) :
        rank = k+1
        turn = turns[k]
        result += turn.bid * rank
    return result

def r1(turns) :
    if turns is None :
        return None
    turns.sort(key=cmp_to_key(compare))
    #print(turns)
    return compute_winnings(turns)

# Note: some_list.sort(key=cmp_to_key(some_function))
# The cmp_to_key function is imported from functools.
# see https://stackoverflow.com/a/57003713/13425151 for a good explanation.



def compare2(turn1: Turn, turn2: Turn):
    return compare(turn1, turn2, True)

def r2(turns) :
    if turns is None :
        return None
    turns.sort(key=cmp_to_key(compare2))
    #print(turns)
    return compute_winnings(turns)



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test_stregth(self):
        self.assertEqual(50, strength('AAAAA'))
        self.assertEqual(40, strength('22122'))
        self.assertEqual(35, strength('K77K7'))
        self.assertEqual(30, strength('K77J7'))
        self.assertEqual(25, strength('22133'))
        self.assertEqual(20, strength('22KJQ'))
        self.assertEqual(15, strength('12345'))
    def test_strength_with_joker(self):
        self.assertEqual(40, strength('KTJJT', joker=True))
        self.assertEqual(50, strength('JJJJJ', joker=True))
        self.assertEqual(50, strength('J3JJJ', joker=True))
        self.assertEqual(50, strength('J3J3J', joker=True))
        self.assertEqual(50, strength('3J3J3', joker=True))
        self.assertEqual(50, strength('33J33', joker=True))
        self.assertEqual(35, strength('11J22', joker=True))
        self.assertEqual(20, strength('1234J', joker=True))
        self.assertEqual(30, strength('123JJ', joker=True))
        self.assertEqual(40, strength('12JJJ', joker=True))
    def test_card_value(self):
        self.assertEqual(5, card_value('5'))
        self.assertEqual(7, card_value('7'))
    def test_card_value_with_joker(self):
        self.assertEqual(1, card_value('J', joker=True))
    def test_lower_than(self):
        self.assertEqual(True, lower_than(Hand('53697'), Hand('76328')))

if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
