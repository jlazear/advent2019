from collections import defaultdict, deque
import intcode



def read_output(outputs, tiles=None):
    tiles = defaultdict(int) if (tiles is None) else tiles
    outputs = deque(outputs)
    while outputs:
        x = outputs.popleft()
        y = outputs.popleft()
        tile_id = outputs.popleft()
        tiles[(x, y)] = tile_id
    return tiles

def display_screen(tiles, c_dict={0: '.', 1: 'X', 2: '#', 3: '-', 4: 'O'}):
    xs = [coord[0] for coord in tiles]
    ys = [coord[1] for coord in tiles]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    
    return '\n'.join([''.join([c_dict[tiles[(x, y)]] for x in range(xmin+1, xmax+1)]) for y in range(ymin, ymax+1)]) + f"\n{tiles[(-1, 0)]}\n\n"

def find_ball(tiles):
    return [coord for coord, value in tiles.items() if value == 4][0]

def find_paddle(tiles):
    return [coord for coord, value in tiles.items() if value == 3][0]

def count_item(tiles, item=2):
    s = 0
    for value in tiles.values():
        if value == item:
            s += 1
    return s

program = intcode.parse_input('input.txt')
program[0] = 2

tiles = None
inputs = [0]
outputs = None
pos = None
base = None
inpos = None
halt = False
waiting = False
i = 0
while not halt:
    while not waiting:
        outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, outputs=outputs, pos=pos, base=base, inpos=inpos)
        i += 1
    tiles = read_output(outputs, tiles)
    # print(display_screen(tiles))
    if not count_item(tiles):
        break
    x_ball, y_ball = find_ball(tiles)
    x_paddle, y_paddle = find_paddle(tiles)
    inpos = 0
    if x_ball < x_paddle:
        inputs = [-1]
    elif x_ball == x_paddle:
        inputs = [0]
    else:
        inputs = [1]

    waiting = False

print(f"score = {tiles[(-1, 0)]}")
