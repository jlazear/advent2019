from copy import deepcopy
import intcode

program = intcode.parse_input('input.txt')

def initialize_nics(program, N=50):
    nics = {}
    for i in range(N):
        program_i = deepcopy(program)
        outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program_i, inputs=[i])
        state = {'program': program_i,
                 'inputs': [],
                 'outputs': outputs,
                 'pos': pos,
                 'base': base,
                 'inpos': 0}
        nics[i] = state
    return nics

def step(nics, address):
    state = nics[address]
    if not state['inputs']:
        state['inputs'] = [-1]
    waiting = False
    while not waiting:
        outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(**state)
        state['outputs'] = outputs
        state['pos'] = pos
        state['base'] = base
        state['inpos'] = inpos
    return state

def step_all(nics):
    for address, state in nics.items():
        step(nics, address)
        state['inpos'] = 0
        state['inputs'] = []
    for address in nics:
        while outputs := nics[address]['outputs']:
            target = outputs.pop(0)
            X = outputs.pop(0)
            Y = outputs.pop(0)
            if target == 255:
                print(f"found out-of-network packet: {target} {X} {Y}")
                return target, X, Y
            nics[target]['inputs'].extend([X, Y])
    return False

nics = initialize_nics(program)
found = False
while not found:
    found = step_all(nics)

target, X, Y = found
print(f"{Y = }")