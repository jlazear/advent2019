def parse_input(fname='input.txt'):
    with open(fname) as f:
        program = f.read().split(',')
        program = [int(x) for x in program]
    return program

def command(program, pos, outputs):
    full_cmd = program[pos]
    cmd = full_cmd % 100
    mode1 = (full_cmd // 100) % 10
    mode2 = (full_cmd // 1000) % 10
    mode3 = (full_cmd // 10000) % 10
    arg1 = pos+1 if mode1 else program[pos+1]
    try:
        arg2 = pos+2 if mode2 else program[pos+2]
    except IndexError:
        arg2 = -1
    try:
        arg3 = pos+3 if mode3 else program[pos+3]
    except IndexError:
        arg3 = -1

    if cmd == 1:  # sum
        program[arg3] = program[arg1] + program[arg2]
        pos += 4
    elif cmd == 2:  # mul
        program[arg3] = program[arg1] * program[arg2]
        pos += 4
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
    return program, pos, outputs


def intcode(program, noun=None, verb=None, inputs=None, copy_program=False, pos=None):
    if copy_program:
        program = program[:]
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
    outputs = []
    while pos < len(program):
        if program[pos] == 3:
            try:
                program[program[pos+1]] = inputs[inpos]
            except IndexError:
                waiting = True
                return outputs, halt, waiting, pos
            pos += 2
            inpos += 1
        elif program[pos] == 99:
            pos += 1
            halt = True
            return outputs, halt, waiting, pos
        else:
            program, pos, outputs = command(program, pos, outputs)
    return outputs, halt, waiting, pos
