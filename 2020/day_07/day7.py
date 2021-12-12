with open('input.txt', 'r') as inputfile :
    rules = inputfile.read().split('\n')

with open('example/input.txt', 'r') as inputfile :
    example = inputfile.read().split('\n')

with open('example/input_2.txt', 'r') as inputfile :
    example2 = inputfile.read().split('\n')

my_color = 'shiny gold'



def rules_dict1(rules) :

    res = {}

    for rule in rules :
        color = rule.split(' bags contain ')[0]
        res[color] = set()

    for dummy in range(2) :
        
        for rule in rules :
            color_concerned, specifications_str = rule.split(' bags contain ')
            specifications = specifications_str.split(', ')
            specifications[-1] = specifications[-1][:-1] # (remove final '.')
            for specification in specifications :
                if specification != 'no other bags' :
                    number_specified = int(specification[0])
                    if number_specified == 1 :
                        color_specified = specification[2:-4]
                    else :
                        color_specified = specification[2:-5]
                    res[color_concerned].add(color_specified)
                    res[color_concerned].update(res[color_specified])
                    for color in res :
                        if color_specified in res[color] :
                            res[color].update(res[color_specified])
    
    return res

def contained_colors(rules) :
    res = []
    color_rules = rules_dict1(rules)
    for color in color_rules :
        if my_color in color_rules[color] :
            res.append(color)

    return set(res)

print(f"Colors that can hold {my_color} in example: {contained_colors(example)}")
print(len(contained_colors(example)))
print(len(contained_colors(rules)))




def rules_dict2(rules) :

    res = {}

    for rule in rules :
        color_concerned, specifications_str = rule.split(' bags contain ')
        specifications = specifications_str.split(', ')
        specifications[-1] = specifications[-1][:-1] # (remove final '.')
        res[color_concerned] = {}
        for specification in specifications :
            if specification != 'no other bags' :
                number_specified = int(specification[0])
                if number_specified == 1 :
                    color_specified = specification[2:-4]
                else :
                    color_specified = specification[2:-5]
                res[color_concerned][color_specified] = number_specified

    return res

def count_bags(color, complete_rules):
    if complete_rules[color] == {} :
        return 0
    else :
        res = 0
        for contained_color in complete_rules[color] :
            number = complete_rules[color][contained_color]
            res += number + number*count_bags(contained_color, complete_rules)
        return res

print(count_bags(my_color, rules_dict2(example)))
print(count_bags(my_color, rules_dict2(example2)))
print(count_bags(my_color, rules_dict2(rules)))
