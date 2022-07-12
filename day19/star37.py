import intcode


def make_map(fname='input.txt'):
    program = intcode.parse_input('input.txt')

    tmap = {}
    for x in range(50):
        for y in range(50):
            inputs = [x, y]
            outputs = None
            pos = None
            base = None

            outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, pos=pos, base=base, outputs=outputs, copy_program=True)
            tmap[(x, y)] = outputs[0]

    return tmap

tmap = make_map()
n = sum([value for value in tmap.values() if value])

print(f"{n = }")