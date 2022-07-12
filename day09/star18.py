from intcode import *

program = parse_input('input.txt')

outputs, halt, waiting, pos, base = intcode(program, inputs=[2])

print(outputs[0])

