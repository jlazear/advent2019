with open('input.txt') as f:
    init_program = f.read().split(',')
    init_program = [int(x) for x in init_program]

def command(program, pos, outputs):
    full_cmd = program[pos]
    cmd = full_cmd % 100
    mode1 = (full_cmd // 100) % 10
    mode2 = (full_cmd // 1000) % 10
    mode3 = (full_cmd // 10000) % 10
    arg1 = pos+1 if mode1 else program[pos+1]
    arg2 = pos+2 if mode2 else program[pos+2]
    arg3 = pos+3 if mode3 else program[pos+3]

    if cmd == 1:  # sum
        program[arg3] = program[arg1] + program[arg2]
        pos += 4
    elif cmd == 2:  # mul
        program[arg3] = program[arg1] * program[arg2]
        pos += 4
    elif cmd == 4:  # output
        outputs.append(program[arg1])
        pos += 2
    return program, pos, outputs


def intcode(noun=None, verb=None, inputs=None, program=None):
    if inputs is None:
        inputs = []
    if program is None:
        program = init_program[:]
    if noun is not None:
        program[1] = noun
    if verb is not None:
        program[2] = verb

    pos = 0
    inpos = 0
    outputs = []
    while pos < len(program):
        if program[pos] == 3:
            program[program[pos+1]] = inputs[inpos]
            pos += 2
        elif program[pos] == 99:
            pos += 1
            break
        else:
            program, pos, outputs = command(program, pos, outputs)
    return outputs


inputs = [1]
outputs = intcode(None, None, inputs, init_program)
print(f"{outputs = }")