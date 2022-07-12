from collections import deque
from itertools import permutations

from intcode import *

program = parse_input('input.txt')

def amplifier_chain(program, phase_str):
    phase_settings = deque([int(x) for x in phase_str])
    value = 0
    while phase_settings:
        phase = phase_settings.popleft()
        inputs = [phase, value]
        values, halt, waiting, pos = intcode(program, inputs=inputs, copy_program=True)
        value = values[0]
    return value

values = []
for phase_str in permutations('01234'):
    values.append(amplifier_chain(program, phase_str))


print(f"{max(values) = }")

