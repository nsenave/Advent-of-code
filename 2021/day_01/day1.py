with open('input.txt') as f :
    puzzle = list(map(int, f.read().split('\n')))

with open('example/input.txt') as f :
    exemple = list(map(int, f.read().split('\n')))


def r1(a) :
    res = 0
    for k in range(1, len(a)) :
        if a[k] > a[k-1] :
            res += 1
    return res

def construire_sommes(liste) :
    res = []
    for k in range(0, len(liste) - 2):
        res.append(sum(liste[k:k+3]))
    return res

def r2(a) :
    return r1(construire_sommes(a))


print(r1(exemple))
print(r1(puzzle))

print(r2(exemple))
print(r2(puzzle))
