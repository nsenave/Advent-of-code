import unittest
from copy import deepcopy



def parse_rule(line:str) :
    id, rule_txt = line.split(': ')
    return id,  [r.replace('"', '').split(' ') for r in rule_txt.split(' | ')]

def parse_rules(lines) :
    rules = {}
    for line in lines :
        id, line_rules = parse_rule(line)
        rules[id] = line_rules
    return rules

def import_input(folder) :
    with open(folder + 'rules.txt', 'r') as inputfile :
        rules = parse_rules(inputfile.read().split('\n'))
    with open(folder + 'messages.txt', 'r') as inputfile :
        messages = inputfile.read().split('\n')
    return rules, messages

puzzle = import_input('')
example = import_input('example/')
example2 = import_input('example2/')

print("Example input:")
print(example)



def check_message(message, rules) :
    message_length = len(message)
    
    stack = [(0, ['0'])]
    
    while stack != [] :

        i, rule_keys = stack.pop(0)

        if i == message_length and rule_keys == [] :
            return True

        else :

            if not (i == message_length or rule_keys == [] or len(rule_keys) > message_length) :

                rule = rules[rule_keys.pop(0)]

                if rule in ([['a']], [['b']]) and message[i] == rule[0][0] :
                    stack.append((i+1, rule_keys))

                else:
                    if rule not in ([['a']], [['b']]) :
                        for sub_rule in rule :
                            stack.append((i, sub_rule + rule_keys))

    return False

def r1(a) :
    rules, messages = a
    return sum(map(lambda x: check_message(x, rules), messages))



def add_loops(rules) :
    rules2 = deepcopy(rules)
    rules2['8'] = [['42'], ['42', '8']]
    rules2['11'] = [['42', '31'], ['42', '11', '31']]
    return rules2

loop_rules = ['8', '11']

def r2(a) :
    rules, messages = a
    return sum(map(lambda x: check_message(x, add_loops(rules)), messages))

    

if __name__ == "__main__" :
    unittest.main(exit=False)

    print("--- Part One ---")
    print(f"Example result: {r1(example)}")
    print(f"Example 2 result: {r1(example2)}")
    print(f"Puzzle answer:  {r1(puzzle)}")
    
    print("--- Part Two ---")
    print(f"Example result: {r2(example)}")
    print(f"Example 2 result: {r2(example2)}")
    print(f"Puzzle answer:  {r2(puzzle)}")
