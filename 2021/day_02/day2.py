def separer(a) :
    res = a.split(' ')
    res[1] = int(res[1])
    return res

with open('input.txt', 'r') as f :
    texte = list(map(separer, f.read().split('\n')))

with open('example/input.txt', 'r') as f :
    exemple = list(map(separer, f.read().split('\n')))


def r1(a) :
    x,y = 0,0
    for etape in a :
        if etape[0] == 'forward':
            y += etape[1]
        elif etape[0] == 'down':
            x += etape[1]
        elif etape[0] == 'up':
            x -= etape[1]
    return x*y

def r2(a) :
    aim = 0
    x,y = 0,0
    for etape in a :
        if etape[0] == 'forward':
            y += etape[1]
            x += etape[1]*aim
        elif etape[0] == 'down':
            aim += etape[1]
        elif etape[0] == 'up':
            aim -= etape[1]
    return x*y

print(r1(exemple))
print(r1(texte))

print(r2(exemple))
print(r2(texte))
