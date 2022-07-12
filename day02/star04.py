with open('input.txt') as f:
    init_program = f.read().split(',')
    init_program = [int(x) for x in init_program]

def run(noun, verb, program=None):
    if program is None:
        program = init_program[:]
    program[1] = noun
    program[2] = verb

    pos = 0
    while pos < len(program):
        if program[pos] == 1:
            program[program[pos+3]] = program[program[pos+1]] + program[program[pos+2]]
        elif program[pos] == 2:
            program[program[pos+3]] = program[program[pos+1]] * program[program[pos+2]]
        elif program[pos] == 99:
            break
        pos += 4
    return program[0]

target_value = 19690720

for noun in range(100):
    for verb in range(100):
        if run(noun, verb) == target_value:
            print(f"{noun = }, {verb = }, answer = {noun}{verb}")