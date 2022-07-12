from intcode import *

program = parse_input('input.txt')

outputs, halt, waiting, pos, base = intcode(program, inputs=[1])

print(outputs[0])

