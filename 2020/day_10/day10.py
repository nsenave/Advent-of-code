with open('input.txt', 'r') as inputfile :
    adapters = list(map(int, inputfile.read().split('\n')))

with open('example/input.txt', 'r') as inputfile :
    example = list(map(int, inputfile.read().split('\n')))

with open('example/input_2.txt', 'r') as inputfile :
    example2 = list(map(int, inputfile.read().split('\n')))

def prepare_data(adapters) :
    adapters.sort()
    adapters = [0] + adapters + [adapters[-1] + 3]
    return adapters

adapters = prepare_data(adapters)
example = prepare_data(example)
example2 = prepare_data(example2)



def differences(adapters) :
    one_diff = 0
    three_diff = 0
    for i in range(1,len(adapters)) :
        diff = adapters[i] - adapters[i-1]
        if diff == 1 :
            one_diff += 1
        elif diff == 3 :
            three_diff += 1
    return one_diff, three_diff

def r1(adapters) :
    one_diff, three_diff = differences(adapters)
    return one_diff * three_diff

print("Part one:")
print(differences(example))
print(differences(example2))
print(r1(adapters))



def f(adapters, i=0) :

    def g(i) :
        return f(adapters, i)

    if known_counts[i] != 0 :
        return known_counts[i]

    else :

        if i+1 == adapters_number :
            return 1
        
        elif i+2 == adapters_number :
            if adapters[i+2] > adapters[i] + 3 :
                return g(i+1)
            else :
                return 1 + g(i+1)
            
        elif i+3 == adapters_number :
            if adapters[i+2] > adapters[i] + 3 :
                return g(i+1)
            else :
                if adapters[i+3] > adapters[i] + 3 :
                    return g(i+2) + g(i+1)
                else :
                    return 1 + g(i+2) + g(i+1)
            
        else :
            known_counts[i+3] = g(i+3)
            known_counts[i+2] = g(i+2)
            known_counts[i+1] = g(i+1)
            if adapters[i+2] > adapters[i] + 3 :
                return g(i+1)
            else :
                if adapters[i+3] > adapters[i] + 3 :
                    return g(i+2) + g(i+1)
                else :
                    return g(i+3) + g(i+2) + g(i+1)

def r2(adapters) :
    global adapters_number, known_counts
    adapters_number = len(adapters) - 1
    known_counts = [0 for n in range(adapters_number)]
    return f(adapters)

print("Part two:")
print(r2(example))
print(r2(example2))
print(r2(adapters))
