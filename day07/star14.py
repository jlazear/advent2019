from collections import deque
from itertools import permutations

from intcode import *

program = parse_input('input.txt')

def amplifier_chain_feedback(program, phase_str):
    phase_settings = deque([int(x) for x in phase_str])
    value = 0

    programA = program[:]
    programB = program[:]
    programC = program[:]
    programD = program[:]
    programE = program[:]

    inputsA, inputsB, inputsC, inputsD, inputsE = [[x,] for x in phase_settings]
    inputsA.append(0)

    outputsA, haltA, waitingA, posA = intcode(programA, inputs=inputsA)
    inputsB.extend(outputsA)
    outputsB, haltB, waitingB, posB = intcode(programB, inputs=inputsB)
    inputsC.extend(outputsB)
    outputsC, haltC, waitingC, posC = intcode(programC, inputs=inputsC)
    inputsD.extend(outputsC)
    outputsD, haltD, waitingD, posD = intcode(programD, inputs=inputsD)
    inputsE.extend(outputsD)
    outputsE, haltE, waitingE, posE = intcode(programE, inputs=inputsE)

    while not any([haltA, haltB, haltC, haltD, haltE]):
        outputsA, haltA, waitingA, posA = intcode(programA, inputs=outputsE, pos=posA)
        outputsB, haltB, waitingB, posB = intcode(programB, inputs=outputsA, pos=posB)
        outputsC, haltC, waitingC, posC = intcode(programC, inputs=outputsB, pos=posC)
        outputsD, haltD, waitingD, posD = intcode(programD, inputs=outputsC, pos=posD)
        outputsE, haltE, waitingE, posE = intcode(programE, inputs=outputsD, pos=posE)

    return outputsE

values = []
for phase_str in permutations('56789'):
    values.append(amplifier_chain_feedback(program, phase_str))


print(f"{max(values) = }")

