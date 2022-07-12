from collections import defaultdict
from copy import deepcopy

def parse_input(fname='input.txt'):
    with open(fname) as f:
        program = f.read().split(',')
        d = defaultdict(int)
        for i, x in enumerate(program):
            d[i] = int(x)
    return d

def command(program, pos, inpos, outputs, inputs, base=0):
    full_cmd = program[pos]
    cmd = full_cmd % 100
    mode1 = (full_cmd // 100) % 10
    mode2 = (full_cmd // 1000) % 10
    mode3 = (full_cmd // 10000) % 10
    if mode1 == 0:
        arg1 = program[pos+1]
    elif mode1 == 1:
        arg1 = pos+1
    elif mode1 == 2:
        arg1 = base + program[pos+1]

    try:
        if mode2 == 0:
            arg2 = program[pos+2]
        elif mode2 == 1:
            arg2 = pos+2
        elif mode2 == 2:
            arg2 = base + program[pos+2]
    except IndexError:
        arg2 = -1
    try:
        if mode3 == 0:
            arg3 = program[pos+3]
        elif mode3 == 1:
            arg3 = pos+3
        elif mode3 == 2:
            arg3 = base + program[pos+3]
    except IndexError:
        arg3 = -1

    # cmd_dict = {1: 'sum', 2: 'mul', 3: 'in ', 4: 'out', 5: 'jit', 6: 'jif', 7: 'lt ', 8: 'eq ', 9: 'rel'}  #DELME
    # print(f"{cmd_dict[cmd]} ({full_cmd} {arg1} {arg2} {arg3}) from ({program[pos]} {program[pos+1]} {program[pos+2]} {program[pos+3]})")  #DELME
    # print(f"{mode1} {mode2} {mode3}")  #DELME
    # print(f"{program[arg1] = } {program[arg2] = } {program[arg3] = }")  #DELME

    if cmd == 1:  # sum
        program[arg3] = program[arg1] + program[arg2]
        pos += 4
    elif cmd == 2:  # mul
        program[arg3] = program[arg1] * program[arg2]
        pos += 4
    elif cmd == 3:  # in
        try:
            program[arg1] = inputs[inpos]
        except IndexError:
            raise IndexError
        pos += 2
        inpos += 1
    elif cmd == 4:  # output
        outputs.append(program[arg1])
        pos += 2
    elif cmd == 5:  # jump if true
        pos = program[arg2] if program[arg1] else pos + 3
    elif cmd == 6:  # jump if false
        pos = program[arg2] if not program[arg1] else pos + 3        
    elif cmd == 7:   # less than
        program[arg3] = 1 if (program[arg1] < program[arg2]) else 0
        pos += 4
    elif cmd == 8:   # equal
        program[arg3] = 1 if (program[arg1] == program[arg2]) else 0
        pos += 4
    elif cmd == 9:   # rel
        base += program[arg1]
        pos += 2
    else:
        raise Exception(f"Invalid command {cmd} at pos {pos}")
    return program, pos, inpos, outputs, inputs, base


def intcode(program, noun=None, verb=None, inputs=None, copy_program=False, pos=None, base=None):
    if copy_program:
        program = deepcopy(program)
    if inputs is None:
        inputs = []
    if noun is not None:
        program[1] = noun
    if verb is not None:
        program[2] = verb

    halt = False
    waiting = False
    pos = 0 if (pos is None) else pos
    inpos = 0
    base = 0 if (base is None) else base
    outputs = []
    while pos < len(program):
        # print(f"\n{pos = } {base = } {program[pos] = } {outputs = }")  #DELME
        if program[pos] == 99:
            pos += 1
            halt = True
            return outputs, halt, waiting, pos, base
        else:
            try:
                program, pos, inpos, outputs, inputs, base = command(program, pos, inpos, outputs, inputs, base)
            except IndexError:
                waiting = True
                return outputs, halt, waiting, pos, base
    return outputs, halt, waiting, pos, base
