from collections import defaultdict, Counter, deque
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
            state[(i, j)] = ord(val)
            if val in '#<>^v':
                scaffolds.add((i, j))
    return state, scaffolds, image

def get_neighbors(coord, scaffolds):
    i, j = coord
    u = (i-1, j)
    d = (i+1, j)
    l = (i, j-1)
    r = (i, j+1)
    neighbors = [x for x in (u, d, l, r) if x in scaffolds]
    return neighbors

def check_neighbor(neighbor, path, scaffolds):
    intersection = (len(get_neighbors(neighbor, scaffolds)) == 4)
    if intersection:
        c = Counter(path)
        return (c[neighbor] < 2)
    else:
        return not neighbor in path

def simple_path(start, scaffolds, startdir='N'):
    delta_from_dir = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    nextdir_from_command = {'N': {'L': 'W', 'R': 'E'},
                            'S': {'L': 'E', 'R': 'W'},
                            'W': {'L': 'S', 'R': 'N'},
                            'E': {'L': 'N', 'R': 'S'}}
    pos = start
    dir = startdir
    commands = []
    count = 0
    while True:
        delta = delta_from_dir[dir]
        nextpos = (pos[0] + delta[0], pos[1] + delta[1])
        if nextpos in scaffolds:
            count += 1
            pos = nextpos
        else:
            if count:
                commands.append(str(count))
            count = 1
            nextdirL = nextdir_from_command[dir]['L']
            deltaL = delta_from_dir[nextdirL]
            nextdirR = nextdir_from_command[dir]['R']
            deltaR = delta_from_dir[nextdirR]
            nextposL = (pos[0] + deltaL[0], pos[1] + deltaL[1])
            nextposR = (pos[0] + deltaR[0], pos[1] + deltaR[1])
            if nextposL in scaffolds:
                commands.append('L')
                dir = nextdirL
                pos = nextposL
            elif nextposR in scaffolds:
                commands.append('R')
                dir = nextdirR
                pos = nextposR
            else:
                break
    return commands


def check_path(path, scaffolds):
    snodes = set(scaffolds)
    spath = set(path)
    return not (snodes - spath)

def dfs(start, scaffolds):
    valids = []
    queue = [(start, [])]
    i = 0  #DELME
    while queue:
        i += 1  #DELME
        coord, path = queue.pop()
        neighbors = get_neighbors(coord, scaffolds)
        good_neighbors = [neighbor for neighbor in neighbors if check_neighbor(neighbor, path, scaffolds)]
        if i % 1000000 == 0:
            print(f"i = {i//1000000}M {coord = } {len(valids) = } {len(queue) = } {len(path) = } {neighbors = } {good_neighbors = }")  #DELME
        if good_neighbors:
            for neighbor in good_neighbors:
                queue.append((neighbor, path + [coord]))
        elif check_path(path + [coord], scaffolds):
            valids.append(path + [coord])
            print(f"====FOUND VALID PATH!==== {len(valids) = } {i = } {len(path) = }")  #DELME
    return valids
        

def sequence_from_path(path, initdir='N'):
    delta_dirs = {(-1, 0): 'N', (1, 0): 'S', (0, 1): 'E', (0, -1): 'W'}
    cmd = {'N': {'W': 'L', 'E': 'R'},
           'S': {'W': 'R', 'E': 'L'},
           'E': {'N': 'L', 'S': 'R'},
           'W': {'N': 'R', 'S': 'L'}}
    
    path = deque(path)
    node = path.popleft()
    dir = initdir
    commands = []
    
    count = 0
    while path:
        nextnode = path.popleft()
        delta = (nextnode[0] - node[0], nextnode[1] - node[1])
        delta_dir = delta_dirs[delta]
        if dir == delta_dir:
            count += 1
        else:
            if count:
                commands.append(str(count))
            commands.append(cmd[dir][delta_dir])
            count = 1
        node = nextnode
        dir = delta_dir
    commands.append(str(count))
    return commands

def test_compression(commands, seq_a, seq_b, seq_c, maxseqlen=None):
    len_a = len(seq_a)
    len_b = len(seq_b)
    len_c = len(seq_c)
    len_tot = len(commands)
    i = 0
    seq = []
    if maxseqlen is not None:
        slen_a = len(','.join(seq_a))
        slen_b = len(','.join(seq_b))
        slen_c = len(','.join(seq_c))
        if slen_a > maxseqlen or slen_b > maxseqlen or slen_c > maxseqlen:
            return False
    while i < len_tot:
        if i + len_a <= len_tot and commands[i:i+len_a] == seq_a:
            seq.append('A')
            i += len_a
        elif i + len_b <= len_tot and commands[i:i+len_b] == seq_b:
            seq.append('B')
            i += len_b
        elif i + len_c <= len_tot and commands[i:i+len_c] == seq_c:
            seq.append('C')
            i += len_c
        else:
            return False
    return seq

def find_next(commands, seq, i0=0):
    len_s = len(seq)
    i = i0
    while i + len_s <= len(commands):
        if commands[i:i+len_s] == seq:
            return i
        i += 1
    return False

def compress(commands, len_min=4, len_max=12, maxseqlen=None):
    for len_a in range(len_min, len_max+1):
        for len_b in range(len_min, len_max+1):
            seq_a = commands[:len_a]
            pos = len_a
            while commands[pos:pos+len_a] == seq_a:
                pos += len_a
            seq_b = commands[pos:pos+len_b]
            pos += len_b
            recheck = True
            while recheck:
                recheck = False
                if commands[pos:pos+len_a] == seq_a:
                    pos += len_a
                    recheck = True
                if commands[pos:pos+len_b] == seq_b:
                    pos += len_b
                    recheck = True
            for len_c in range(len_min, len_max+1):
                seq_c = commands[pos:pos+len_c]
                if seq := test_compression(commands, seq_a, seq_b, seq_c, maxseqlen=maxseqlen):
                    return seq, seq_a, seq_b, seq_c
    return False

def run_robot(seq_compressed, seq_a, seq_b, seq_c, fname='input.txt'):
    program = intcode.parse_input('input.txt')
    program[0] = 2

    input_str = f"{','.join(seq_compressed)}\n{','.join(seq_a)}\n{','.join(seq_b)}\n{','.join(seq_c)}\nn\n"
    inputs = list(map(ord, input_str))

    outputs = None
    pos = None
    base = None
    halt = False
    inpos = 0

    while not halt:
        outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, pos=pos, base=base, outputs=outputs, inpos=inpos)

    return outputs

state, scaffolds, image = make_map()

dirdict = {'^': 'N', '>': 'E', 'v': 'S', '<': 'W'}
start = [coord for coord, val in state.items() if val not in tuple(map(ord, tuple('.#')))][0]
startdir = dirdict[chr(state[start])]
commands = simple_path(start, scaffolds, startdir)
seq_compressed, seq_a, seq_b, seq_c = compress(commands, maxseqlen=20)
outputs = run_robot(seq_compressed, seq_a, seq_b, seq_c)
s_outputs = ''.join([chr(c) if c < 0x110000 else str(c) for c in outputs])
print(s_outputs)

# if you want to find all of the solutions, set this to True... takes about an hour though
# only the simple solution above actually works though! All 2000+ other routes are not sufficiently compressible
find_all_solutions = False
if find_all_solutions:
    solutions = []
    valids = dfs(start, scaffolds)
    for path in valids:
        commands = sequence_from_path(path)
        compress_out = compress(commands, maxseqlen=20)
        if compress_out:
            solutions.append(compress_out)

print(f"found {len(solutions)} solutions, stored in `solutions`")