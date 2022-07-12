import intcode

program = intcode.parse_input('input.txt')

state = {'program': program,
            'inputs': [],
            'outputs': [],
            'pos': 0,
            'base': 0,
            'inpos': 0}

def step(state, command=''):
    inputs = [ord(c) for c in command] + [ord('\n')]
    waiting = False
    halt = False
    state['inputs'] = inputs
    state['inpos'] = 0
    while not waiting and not halt:
        outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(**state)
        state['outputs'] = outputs
        state['pos'] = pos
        state['base'] = base
        state['inpos'] = inpos
    response = ''.join(map(chr, outputs))
    state['outputs'] = []
    return response, state

while True:
    command = input('>>> ')
    if command == 'quit': break
    response, state = step(state, command)
    print(response)
    print(f"prev> {command}")
    
# answer = klein bottle + astrolabe + whirled peas + tambourine + hologram