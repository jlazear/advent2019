def parse_input(fname='input.txt'):
    s = ''
    for c in open(fname).read():
        if c in '.#':
            s += c
    return s

def print_state(state, nrows=5, ncols=5):
    s = ''
    for i, c in enumerate(state):
        if i != 0 and i % ncols == 0:
            s += '\n'
        s += c
    return s

def biodiversity_rating(state):
    s = 0
    for i, c in enumerate(state):
        s += 2**i * (1 if c == '#' else 0)
    return s

def rc_from_i(i, nrows=5, ncols=5):
    row, col = i // ncols, i % nrows
    return row, col

def i_from_rc(row, col, nrows=5, ncols=5):
    if row < 0 or row > nrows-1 or col < 0 or col > ncols-1:
        return -1
    return row*ncols + col

def get_neighbors(i, nrows=5, ncols=5):
    row, col = rc_from_i(i)

    iu = i_from_rc(row-1, col, nrows=nrows, ncols=ncols)
    id = i_from_rc(row+1, col, nrows=nrows, ncols=ncols)
    il = i_from_rc(row, col-1, nrows=nrows, ncols=ncols)
    ir = i_from_rc(row, col+1, nrows=nrows, ncols=ncols)

    neighbors = [i for i in (iu, id, il, ir) if i >= 0]
    return neighbors

def update(state, nrows=5, ncols=5):
    newstate = []
    for i, value in enumerate(state):
        neighbors = get_neighbors(i, nrows=nrows, ncols=ncols)
        n = sum(state[neighbor] == '#' for neighbor in neighbors)
        if value == '#' and not (n == 1):
            newstate.append('.')
        elif value == '.' and n in (1, 2):
            newstate.append('#')
        else:
            newstate.append(value)
    newstate = ''.join(newstate)
    return newstate

state = parse_input('input.txt')
seen = set()
while state not in seen:
    seen.add(state)
    state = update(state)

print(f"{biodiversity_rating(state) = }")