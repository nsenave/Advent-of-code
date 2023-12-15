import os.path
import unittest

def parse_input(file_path: str) :
    if not os.path.exists(file_path) :
        return None
    with open(file_path, 'r') as f :
        return f.read().split(',')

puzzle = parse_input('input.txt')
example = parse_input('input-example.txt')

print("Example input:")
print(example)



def holiday_ascii_string_helper(string: str) -> int:
    res = 0
    for c in string:
        res += ord(c)
        res *= 17
        res %= 256
    return res

def r1(a) :
    if a is None :
        return None
    result = 0
    for step in a:
        result += holiday_ascii_string_helper(step)
    return result



def fill_boxes(init_sequence: str) -> list:
    boxes = [[] for _ in range(256)]
    for step in init_sequence:
        if '=' in step:
            label, focal_length = step[:-2], int(step[-1])
            insert_lens(boxes, label, focal_length)
            continue
        if '-' in step:
            label = step[:-1]
            remove_lens(boxes, label)
            continue
        raise ValueError(f"Step {step} does not contain either '=' or '-'.")
    return boxes

def insert_lens(boxes: list, label: str, focal_length: int) -> None:
    index = holiday_ascii_string_helper(label)
    box = boxes[index]
    current_lens = (label, focal_length)
    if not box: # i.e. is empty
        box.append(current_lens)
        return None
    label_index = index_of_label_in_box(box, label)
    if label_index is None:
        box.append(current_lens)
        return None
    box[label_index] = current_lens

def remove_lens(boxes: list, label: str) -> None:
    index = holiday_ascii_string_helper(label)
    box = boxes[index]
    label_index = index_of_label_in_box(box, label)
    if label_index is not None:
        box.pop(label_index)

def index_of_label_in_box(box: list, label: str) -> int:
    for i in range(len(box)):
        lens = box[i]
        if lens[0] == label:
            return i
    return None


def focusing_power(lens: tuple, slot_number: int, box_number: int) -> int:
    return (1 + box_number) * (1 + slot_number) * lens[1]

def r2(a) :
    if a is None :
        return None
    boxes = fill_boxes(a)
    result = 0
    for box_number in range(256):
        box = boxes[box_number]
        for slot_number in range(len(box)):
            lens = box[slot_number]
            result += focusing_power(lens, slot_number, box_number)
    return result



class TestsOfToday(unittest.TestCase):

    def setUp(self):
        pass

    def test1(self):
        self.assertEqual(holiday_ascii_string_helper("HASH"), 52)
    
    def test2(self):
        self.assertEqual(holiday_ascii_string_helper('rn=1'), 30)
        self.assertEqual(holiday_ascii_string_helper('cm-'), 253)
        self.assertEqual(holiday_ascii_string_helper('qp=3'), 97)
        self.assertEqual(holiday_ascii_string_helper('cm=2'), 47)
        self.assertEqual(holiday_ascii_string_helper('qp-'), 14)
        self.assertEqual(holiday_ascii_string_helper('pc=4'), 180)
        self.assertEqual(holiday_ascii_string_helper('ot=9'), 9)
        self.assertEqual(holiday_ascii_string_helper('ab=5'), 197)
        self.assertEqual(holiday_ascii_string_helper('pc-'), 48)
        self.assertEqual(holiday_ascii_string_helper('pc=6'), 214)
        self.assertEqual(holiday_ascii_string_helper('ot=7'), 231)
    
    def test3(self):
        self.assertEqual(holiday_ascii_string_helper('rn'), 0)
        self.assertEqual(holiday_ascii_string_helper('qp'), 1)
        self.assertEqual(holiday_ascii_string_helper('cm'), 0)
        self.assertEqual(holiday_ascii_string_helper('pc'), 3)
        self.assertEqual(holiday_ascii_string_helper('ot'), 3)
        self.assertEqual(holiday_ascii_string_helper('ab'), 3)



if __name__ == '__main__':
    unittest.main(exit=False)
    
    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
