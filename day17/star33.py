from collections import defaultdict
import intcode


def make_map(fname='input.txt'):
    program = intcode.parse_input('input.txt')

    inputs = None
    outputs = None
    pos = None
    base = None
    halt = False

    while not halt:
        outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, pos=pos, base=base, outputs=outputs)

    state = defaultdict(lambda: 46)
    scaffolds = set()

    image = ''.join([chr(out) for out in outputs])
    for i, row in enumerate(image.split('\n')):
        for j, val in enumerate(row):
            state[(j, i)] = ord(val)
            if val in '#<>^v':
                scaffolds.add((j, i))
    return state, scaffolds, image

def check_intersection(coord, state):
    i, j = coord
    adjacents = [(i-1, j), (i+1, j), (i, j+1), (i, j-1)]
    return sum([state[coord2] == ord('#') for coord2 in adjacents]) == 4

state, scaffolds, image = make_map()

s = 0
for coord in scaffolds:
    if check_intersection(coord, state):
        s += coord[0]*coord[1]

print(image)
print(f"{s = }")