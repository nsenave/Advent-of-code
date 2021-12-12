with open('boarding_passes.txt', 'r') as inputfile :
    boarding_passes = inputfile.read().split('\n')

with open('example/boarding_passes.txt', 'r') as inputfile :
    example = inputfile.read().split('\n')

print(example)

class BoardingRowException(Exception) :
    pass

def get_row(boarding_pass) :
    rows = [r for r in range(128)]
    for k in range(0,7) :
        if boarding_pass[k] == 'F' :
            rows = rows[:len(rows)//2]
        elif boarding_pass[k] == 'B' :
            rows = rows[len(rows)//2:]
        else :
            raise BoardingRowException
    #print(rows)
    return rows.pop()

class BoardingColumnException(Exception) :
    pass

def get_column(boarding_pass) :
    columns = [c for c in range(8)]
    for k in range(7,10) :
        if boarding_pass[k] == 'L' :
            columns = columns[:len(columns)//2]
        elif boarding_pass[k] == 'R' :
            columns = columns[len(columns)//2:]
        else :
            raise BoardingColumnException
    #print(columns)
    return columns.pop()

def get_id(boarding_pass) :
    return get_row(boarding_pass)*8 + get_column(boarding_pass)

def r1(boarding_passes) :
    return max( list(map(get_id, boarding_passes)) )

print(list(map(get_id, example)))

print(r1(boarding_passes))


unoccupied_rows = [r for r in range(128)]

id_list = [id for id in range(128*8 + 8)]

for boarding_pass in boarding_passes :
    row = get_row(boarding_pass)
    column = get_column(boarding_pass)
    seat_id = row*8 + column
    #
    if row in unoccupied_rows :
        unoccupied_rows.pop(unoccupied_rows.index(row))
    #
    i = id_list.index(seat_id)
    id_list.pop(i)

print(unoccupied_rows)

for row in unoccupied_rows :
    for c in range(0,8) :
        seat_id = row*8 + c
        i = id_list.index(seat_id)
        id_list.pop(i)

print(id_list)
