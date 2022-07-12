from collections import defaultdict
import intcode

def check_coord(x, y, program):
    inputs = [x, y]

    outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, copy_program=True)
    return outputs[0]

def find_first_col(y, program, x0=0):
    out = 0
    x = x0 - 1
    while not out:
        x += 1
        out = check_coord(x, y, program)
    return x

def find_first_row(x, program, y0=0):
    out = 0
    y = y0 - 1
    while not out:
        y += 1
        out = check_coord(x, y, program)
    return y


def check_fit(x, y, program, side=99, bottom_edge=True):
    if y < side:
        return False
    if bottom_edge:
        bottomleft = check_coord(x, y, program)
        bottomright = check_coord(x+side, y, program)
        topleft = check_coord(x, y-side, program)
        topright = check_coord(x+side, y-side, program)
    else:
        topright = check_coord(x, y, program)
        topleft = check_coord(x-side, y, program)
        bottomleft = check_coord(x-side, y+side, program)
        bottomright = check_coord(x, y+side, program)

    return all([bottomleft, bottomright, topleft, topright])


program = intcode.parse_input('input.txt')
fits = False
y = 100
x = 0
while not fits:
    y += 1
    x = find_first_col(y, program, x0=x)
    fits = check_fit(x, y, program, side=99, bottom_edge=True)
    # print(f"LL = ({x}, {y}), {fits = }")

print(f"BOTTOM EDGE {10000*x + (y-99) = }")

fits = False
y = 0
x = 100
while not fits:
    x += 1
    y = find_first_row(x, program, y0=y)
    fits = check_fit(x, y, program, side=99, bottom_edge=False)
    # print(f"LL = ({x}, {y}), {fits = }")

print(f"TOP EDGE {10000*(x-99) + y = }")