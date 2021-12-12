with open('input.txt', 'r') as inputfile :
    sequence = list(map(int, inputfile.read().split('\n')))

with open('example/input.txt', 'r') as inputfile :
    example = list(map(int, inputfile.read().split('\n')))


window_length = 25

def check_number(n, previous, window_length) :
    res = False
    i = 0
    while i < window_length and not res :
        j = i+1
        while j < window_length and not res :
            #print(previous[i], previous[j])
            if previous[i] + previous[j] == n :
                res = True
                #print(f"{previous[i]} + {previous[j]} = {n}")
            j += 1
        i += 1
    return res

def find_index(sequence, window_length) :
    sequence_lenght = len(sequence)
    is_valid = True
    i = window_length
    while is_valid and i < sequence_lenght :
        is_valid = check_number(sequence[i], sequence[i-window_length:i], window_length)
        i += 1
    return i-1

def r1(sequence, window_length) :
    i = find_index(sequence, window_length)
    return sequence[i]

print(r1(example, 5))
print(r1(sequence, 25))


def find_contiguous_sum(sequence, window_length) :
    i = find_index(sequence, window_length)
    aimed_number = sequence[i]
    sequence = sequence[:i]
    sequence_lenght = len(sequence)
    for sum_length in range(2, sequence_lenght) :
        for start in range(0, sequence_lenght - sum_length) :
            if sum(sequence[start:start+sum_length]) == aimed_number :
                return min(sequence[start:start+sum_length]) + max(sequence[start:start+sum_length])

print(find_contiguous_sum(example, 5))
print(find_contiguous_sum(sequence, 25))
