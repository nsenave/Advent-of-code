from copy import deepcopy

with open('input.txt') as inputfile :
    instructions_init = inputfile.read().split('\n')

with open('example/input.txt') as inputfile :
    example = inputfile.read().split('\n')

class BadInstructionTypeException(Exception) :
    pass


def compute_program(instructions) :

    visited_lines = [0 for i in range(len(instructions))]

    acc_value = 0
    terminate = False

    i = 0
    while visited_lines[i] == 0 and not terminate :
        #
        visited_lines[i] += 1
        #
        instruction = instructions[i]
        instruction_type, instruction_value = instruction.split(' ')
        value_sign, value_int = instruction_value[0], int(instruction_value[1:])
        #
        if instruction_type == 'acc' :
            if value_sign == '+' :
                acc_value += value_int
            elif value_sign == '-' :
                acc_value -= value_int
            else :
                print('OSKOUR')
            i += 1
        elif instruction_type == 'jmp' :
            if value_sign == '+' :
                i += value_int
            elif value_sign == '-' :
                i -= value_int
            else :
                print('OSKOUR')
        elif instruction_type == 'nop' :
            i += 1
        elif instruction_type == 'end' :
            terminate = True
        else :
            raise BadInstructionTypeException()

    #print(i, instructions[i])
    return terminate, acc_value

print(compute_program(example))
print(compute_program(instructions_init))


example.append('end +0')
instructions_init.append('end +0')

def r2(instructions_init) :

    program_length = len(instructions_init)

    has_terminated = False

    i = 0
    while i < program_length and not has_terminated :
        instructions = deepcopy(instructions_init)
        instruction = instructions[i]
        instruction_type = instruction.split(' ')[0]
        if instruction_type == 'jmp' :
            instructions[i] = 'nop' + instructions[i][3:]
        elif instruction_type == 'nop' :
            instructions[i] = 'jmp' + instructions[i][3:]
        has_terminated, acc_final_value = compute_program(instructions)
        i += 1

    print(i-1, instructions[i-1])
    return(acc_final_value)

print(r2(example))
print(r2(instructions_init))
