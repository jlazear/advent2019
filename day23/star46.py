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

def is_idle(nics, new_outputs=True):
    return (not any([state['inputs'] for state in nics.values()])) and (not new_outputs)

def step_all(nics, nat_X=0, nat_Y=0, new_outputs=True):
    if is_idle(nics, new_outputs):
        print(f"delivering {nat_X} {nat_Y} to NAT")
        nics[0]['inputs'] = [nat_X, nat_Y]
    else:
        for address, state in nics.items():
            step(nics, address)
            state['inpos'] = 0
            state['inputs'] = []
    new_outputs = False
    for address in nics:
        while outputs := nics[address]['outputs']:
            new_outputs = True
            target = outputs.pop(0)
            X = outputs.pop(0)
            Y = outputs.pop(0)
            if target == 255:
                print(f"found NAT packet: {target} {X} {Y}")
                nat_X, nat_Y = X, Y
            else:
                nics[target]['inputs'].extend([X, Y])
    return nat_X, nat_Y, new_outputs

nics = initialize_nics(program)
nat_X = nat_Y = 0
new_outputs = True
while True:
    nat_X, nat_Y, new_outputs = step_all(nics, nat_X=nat_X, nat_Y=nat_Y, new_outputs=new_outputs)
