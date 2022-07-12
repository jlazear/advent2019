from collections import defaultdict

def parse_input(fname='input.txt'):
    state = defaultdict(int)
    depth = 0
    s = ''
    for c in open(fname).read():
        if c in '.#':
            s += c
    for i, c in enumerate(s):
        row, col = rc_from_i(i)
        state[(row, col, depth)] = 1 if c == '#' else 0
    return state

def print_state(state, depth):
    return '\n'.join([''.join(['#' if state[(i, j, depth)] else '.' for j in range(5)]) for i in range(5)])

def num_bugs(state):
    return sum([value for value in state.values()])

def rc_from_i(i, nrows=5, ncols=5):
    row, col = i // ncols, i % nrows
    return row, col

def get_neighbors(coord):
    row, col, depth = coord
    if row == col == 2:
        return []
    
    iu = row-1, col
    id = row+1, col
    il = row, col+1
    ir = row, col-1

    neighbors = []
    for newrow, newcol in (iu, id, il, ir):
        if newrow == -1:
            newneighbors = [(1, 2, depth-1)]
        elif newrow == 5:
            newneighbors = [(3, 2, depth-1)]
        elif newcol == -1:
            newneighbors = [(2, 1, depth-1)]
        elif newcol == 5:
            newneighbors = [(2, 3, depth-1)]
        elif newrow == newcol == 2:
            if row == 2:
                newcol = 0 if newcol > col else 4
                newneighbors = [(r, newcol, depth+1) for r in range(5)]
            elif col == 2:
                newrow = 0 if newrow > row else 4
                newneighbors = [(newrow, c, depth+1) for c in range(5)]
        else:
            newneighbors = [(newrow, newcol, depth)]
        neighbors.extend(newneighbors)
    return neighbors

def update(state):
    newstate = state.copy()
    depths = [depth for (_, _, depth), value in state.items() if value]
    mindepth, maxdepth = min(depths)-1, max(depths)+1
    for coord in ((row, col, depth) for row in range(5) for col in range(5) for depth in range(mindepth, maxdepth+1)):
        value = state[coord]
        neighbors = get_neighbors(coord)
        n = sum(state[neighbor] for neighbor in neighbors)
        if value and not (n == 1):
            newstate[coord] = 0
        elif not value and n in (1, 2):
            newstate[coord] = 1
        else:
            newstate[coord] = value
    return newstate

state = parse_input('input.txt')
for i in range(200):
    # print(f"{i = } {num_bugs(state) = }")
    state = update(state)
print(f"{i+1 = } {num_bugs(state) = }")