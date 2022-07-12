with open('input.txt') as f:
    program = f.read().split(',')
    program = [int(x) for x in program]
program[1] = 12
program[2] = 2

pos = 0
while pos < len(program):
    if program[pos] == 1:
        program[program[pos+3]] = program[program[pos+1]] + program[program[pos+2]]
    elif program[pos] == 2:
        program[program[pos+3]] = program[program[pos+1]] * program[program[pos+2]]
    elif program[pos] == 99:
        break
    pos += 4

print(f"{program[0] = }")