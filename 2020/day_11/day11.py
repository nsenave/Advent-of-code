from numpy import array, copy

with open('input.txt', 'r') as inputfile :
    seats_map = array([list(line) for line in inputfile.read().split('\n')])

with open('example/input.txt', 'r') as inputfile :
    example = array([list(line) for line in inputfile.read().split('\n')])

class InvalidSeatException(Exception) :
    pass



def increment(seats_map) :
    has_changed = False
    previous_map = copy(seats_map)
    for i in range(dim_x) :
        if i == 0 :
            dx_list = (0,1)
        elif i == dim_x - 1 :
            dx_list = (-1,0)
        else :
            dx_list = (-1, 0, 1)
        for j in range(dim_y) :
            if j == 0 :
                dy_list = (0,1)
            elif j == dim_y - 1 :
                dy_list = (-1,0)
            else :
                dy_list = (-1, 0, 1)
            #
            occupied_adjacent_seats = 0
            for dx in dx_list :
                for dy in dy_list :
                    if (dx,dy) != (0,0) :
                        neighbour_coords = (i+dx,j+dy)
                        if previous_map[neighbour_coords] == '#' :
                            occupied_adjacent_seats += 1
            #
            if seats_map[i,j] == 'L' :
                if occupied_adjacent_seats == 0 :
                    seats_map[i,j] = '#'
                    has_changed = True
            elif seats_map[i,j] == '#' :
                if occupied_adjacent_seats >= 4 :
                    seats_map[i,j] = 'L'
                    has_changed = True
            elif seats_map[i,j] == '.' :
                pass
            else :
                raise InvalidSeatException()
    return has_changed



def find_visible_seats(seats_map, i, j) :
    """Return the list of coords of the seats visible from (i,j)."""
    res = []
    # Up
    up = 1
    seat_found = False
    while (i - up >= 0) and not seat_found :
        if seats_map[i-up, j] != '.' :
            seat_found = True
            res.append( (i - up, j) )
        else :
            up += 1
    # Bottom
    down = 1
    seat_found = False
    while (i + down < dim_x) and not seat_found :
        if seats_map[i+down, j] != '.' :
            seat_found = True
            res.append( (i + down, j) )
        else :
            down += 1
    # Left
    left = 1
    seat_found = False
    while (j - left >= 0) and not seat_found :
        if seats_map[i, j-left] != '.' :
            seat_found = True
            res.append( (i, j - left) )
        else :
            left += 1
    # Right
    right = 1
    seat_found = False
    while (j + right < dim_y) and not seat_found :
        if seats_map[i, j+right] != '.' :
            seat_found = True
            res.append( (i, j + right) )
        else :
            right += 1
    # Up-left diagonal
    up = 1
    left = 1
    seat_found = False
    while (i - up >= 0) and (j - left >= 0) and not seat_found :
        if seats_map[i-up, j-left] != '.' :
            seat_found = True
            res.append( (i - up, j - left) )
        else :
            up += 1
            left += 1
    # Up-right diagonal
    up = 1
    right = 1
    seat_found = False
    while (i - up >= 0) and (j + right < dim_y) and not seat_found :
        if seats_map[i-up, j+right] != '.' :
            seat_found = True
            res.append( (i - up, j + right) )
        else :
            up += 1
            right += 1
    # Bottom-left diagonal
    down = 1
    left = 1
    seat_found = False
    while (i + down < dim_x) and (j - left >= 0) and not seat_found :
        if seats_map[i+down, j-left] != '.' :
            seat_found = True
            res.append( (i + down, j - left) )
        else :
            down += 1
            left += 1
    # Bottom-right diagonal
    down = 1
    right = 1
    seat_found = False
    while (i + down < dim_x) and (j + right < dim_y) and not seat_found :
        if seats_map[i+down, j+right] != '.' :
            seat_found = True
            res.append( (i + down, j + right) )
        else :
            down += 1
            right += 1
    #
    return res

def increment_bis(seats_map) :
    has_changed = False
    previous_map = copy(seats_map)
    for i in range(dim_x) :
        for j in range(dim_y) :
            #
            occupied_adjacent_seats = 0
            for coords in find_visible_seats(seats_map, i, j) :
                if previous_map[coords] == '#' :
                    occupied_adjacent_seats += 1
            #
            if seats_map[i,j] == 'L' :
                if occupied_adjacent_seats == 0 :
                    seats_map[i,j] = '#'
                    has_changed = True
            elif seats_map[i,j] == '#' :
                if occupied_adjacent_seats >= 5 :
                    seats_map[i,j] = 'L'
                    has_changed = True
            elif seats_map[i,j] == '.' :
                pass
            else :
                raise InvalidSeatException()
    return has_changed



def r(seats_map_init, increment_function) :
    global dim_x, dim_y
    dim_x, dim_y = seats_map_init.shape

    seats_map = copy(seats_map_init)

    step = 0
    stop = 1000
    while increment_function(seats_map) :
        step += 1
        if step >= stop :
            print('BREAK')
            break

    occupied_seats_number = 0
    for i in range(dim_x) :
        for j in range(dim_y) :
            if seats_map[i,j] == '#' :
                occupied_seats_number += 1
    return occupied_seats_number

print(r(example, increment))
print(r(seats_map, increment))

print(r(example, increment_bis))
print(r(seats_map, increment_bis))
