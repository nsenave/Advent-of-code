from numpy import array,zeros,sum
from copy import deepcopy

initial_state = """\
.......#
....#...
...###.#
#...###.
....##..
##.#..#.
###.#.#.
....#...\
"""

"""
Rules :

    If a cube is active and exactly 2 or 3 of its neighbors are also active,
    the cube remains active.
    Otherwise, the cube becomes inactive.

    If a cube is inactive but exactly 3 of its neighbors are active,
    the cube becomes active. Otherwise, the cube remains inactive.

"""

with open('input.txt', 'r') as inputfile :
    input_rows = inputfile.readlines()
    initial_plan = []
    for row in input_rows :
        initial_plan.append( list(row.replace('\n','')) )

print(initial_plan)

initial_size = len(initial_plan[0])

final_step = 6

space_size = initial_size + 2 *(final_step + 2)

ndim = 4

grille = zeros(tuple([space_size] * ndim), dtype = int)

center = space_size//2

for x in range(initial_size) :
    for y in range(initial_size) :
        if initial_plan[x][y] == '#' :
            grille[center,center,center - initial_size//2 + x, center - initial_size//2 + y] = 1

print(sum(grille))

def get_neighbours_coords(x,y,z,w) :
    res = []
    for dx in (-1, 0, 1) :
        for dy in (-1, 0, 1) :
            for dz in (-1, 0, 1) :
                for dw in (-1, 0, 1) :
                    if (dx,dy,dz,dw) != (0,0,0,0) :
                        res.append( (x+dx, y+dy, z+dz, w+dw) )
    return res

for step in range(0, final_step) :
    print(f"setp {step}")
    # center - (initial_size//2+step), center + (initial_size//2+step)+1
    grille_old = deepcopy(grille)
    for x in range(space_size-1) :
        for y in range(space_size-1) :
            for z in range(space_size-1) :
                for w in range(space_size-1) :

                    active_neighbours = 0
                    neighbours_coords = get_neighbours_coords(x,y,z,w)
                    for coords in neighbours_coords :
                        if grille_old[coords] == 1 :
                            active_neighbours += 1
                    coords = (x,y,z,w)
                    if grille_old[coords] == 1 and (active_neighbours not in (2,3)) :
                        grille[coords] = 0
                    if grille_old[coords] == 0 and active_neighbours == 3 :
                        grille[coords] = 1

print(f"Resultat : {sum(grille)}")
