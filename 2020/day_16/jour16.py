import csv

data_folder = ''

with open(data_folder + 'rules.txt') as inputfile :
    rules_text = inputfile.readlines()

rules = []
for row in rules_text :
    rule_text = row.split(': ')[1].split(' or ')
    rule1 = list(map(int, rule_text[0].split('-')))
    rule2 = list(map(int, rule_text[1].split('-')))
    rules.append(rule1 + rule2)
rules_number = len(rules)
#print(rules)

"""
with open('tickets.csv') as csv_inputfile:
    csv_reader = csv.reader(csv_inputfile, delimiter=',')
    line_count = 0
    res = 0
    for row in csv_reader:
        ticket = list(map(int, row))
        for ticket_value in ticket :
            is_valid = False
            j = 0
            while (not is_valid) and j < rules_number :
                rule = rules[j]
                if (rule[0] <= ticket_value <= rule[1]) or (rule[2] <= ticket_value <= rule[3]) :
                    is_valid = True
                j += 1
            if not is_valid :
                res += ticket_value
        line_count += 1
    print(res)
"""

with open(data_folder + 'tickets.csv') as csv_inputfile:
    csv_reader = csv.reader(csv_inputfile, delimiter=',')
    line_count = 0
    valid_tickets = []
    for row in csv_reader:
        ticket = list(map(int, row))
        is_valid_ticket = True
        for ticket_value in ticket :
            is_valid_value = False
            j = 0
            while (not is_valid_value) and j < rules_number :
                rule = rules[j]
                if (rule[0] <= ticket_value <= rule[1]) or (rule[2] <= ticket_value <= rule[3]) :
                    is_valid_value = True
                j += 1
            if not is_valid_value :
                is_valid_ticket = False
        if is_valid_ticket :
            valid_tickets.append(ticket)
        line_count += 1

print(len(valid_tickets))

rules_positions = [[j for j in range(rules_number)] for n in range(rules_number)]

#print(rules_positions)

for ticket in valid_tickets :
    for j1 in range(rules_number) :
        ticket_value = ticket[j1]
        for j in range(rules_number) :
            rule = rules[j]
            if not ( (rule[0] <= ticket_value <= rule[1]) or (rule[2] <= ticket_value <= rule[3]) ) :
                if j1 in rules_positions[j] :
                    rules_positions[j].remove(j1)

res = [0 for j in range(rules_number)]

for k in range(rules_number) :
    j = list(map(len, rules_positions)).index(1)
    position = rules_positions[j][0]
    res[position] = j
    for positions_list in rules_positions :
        if position in positions_list :
            positions_list.remove(position)

print(res)

my_ticket = [127,83,79,197,157,67,71,131,97,193,181,191,163,61,53,89,59,137,73,167]

res_final = 1
for j in (0,1,2,3,4,5) :
    position = res.index(j)
    res_final *= my_ticket[position]

print(res_final)
