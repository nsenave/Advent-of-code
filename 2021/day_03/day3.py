import numpy as np
from copy import deepcopy

def line_split(line) :
    res = line
    return list(map(int, list(res)))

with open('input.txt', 'r') as f :
    puzzle = np.array(list(map(line_split, f.read().split('\n'))))

with open('example/input.txt', 'r') as f :
    example = np.array(list(map(line_split, f.read().split('\n'))))

print(example)



def gamma(liste) -> str :
    res = ''
    n,m = liste.shape
    for j in range(0,m) :
        sum1 = sum(liste[:,j])
        if sum1 >= n - sum1 :
            res += '1'
        else :
            res += '0'
    return res

def eps_from_gamma(binary:str) :
    res = ''
    for b in binary :
        if b=='1' :
            res += '0'
        else :
            res += '1'
    return res

def eps(liste) -> str :
    return eps_from_gamma(gamma(liste))

def dec(binary:str) :
    return int(binary, 2)

print(gamma(example), dec(gamma(example)))
print(eps(example), dec(eps(example)))

def r1(a) :
    return dec(gamma(a)) * dec(eps(a))

print(r1(example))
print(r1(puzzle))



def array_to_str(a) :
    res = ''
    for x in a :
        res += str(x)
    return res

def step(rate_function, liste, j=0) :
    if len(liste) == 1 or j == liste.shape[1] :
        return array_to_str(liste[0,:])
    else :
        b = rate_function(liste)[j]
        i = 0
        while i < len(liste) :
            if liste[i,j] != int(b) :
                liste = np.delete(liste, (i), axis=0)
            else :
                i += 1
        return step(rate_function, liste, j+1)

def ox(liste_init) -> str :
    liste = deepcopy(liste_init)
    return step(gamma, liste)

def co2(liste_init) -> str :
    liste = deepcopy(liste_init)
    return step(eps, liste)

print(ox(example), dec(ox(example)))
print(co2(example), dec(co2(example)))

def r2(a) :
    return dec(ox(a)) * dec(co2(a))

print(r2(example))
print(r2(puzzle))
