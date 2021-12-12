with open('input.txt', 'r') as inputfile :
    groups = inputfile.read().split('\n\n')

with open('example/input.txt', 'r') as inputfile :
    example = inputfile.read().split('\n\n')

print(example)

def r1(groups) :
    res = 0
    for group in groups :
        caract_list = list(group)
        while '\n' in caract_list :
            caract_list.remove('\n')
        res += len(set(caract_list))
    return res

print(r1(example))
print(r1(groups))

def r2(groups) :
    res2 = 0
    for group in groups :
        group_answers = group.split('\n')
        yeses = {}
        for answer in group_answers :
            for yes in answer :
                if yes not in yeses :
                    yeses[yes] = 1
                else :
                    yeses[yes] += 1
        collective_yeses = []
        for answer in yeses :
            if yeses[answer] == len(group_answers) :
                collective_yeses.append(answer)
        res2 += len(collective_yeses)
    return res2

print(r2(example))
print(r2(groups))
