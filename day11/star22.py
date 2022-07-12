from collections import defaultdict
import intcode

program = intcode.parse_input('input.txt')

dxdy_dict = {0: (0, 1),   # up
             1: (1, 0),   # right
             2: (0, -1),  # down
             3: (-1, 0)}  # left

direction = 0
coord = (0, 0)
image = defaultdict(int)
image[coord] = 1
halt = False
waiting = True
pos = 0
base = 0


inputs = [image[coord]]
while not halt:
    outputs, halt, waiting, pos, base = intcode.intcode(program, inputs=inputs, pos=pos, base=base)
    color, delta = outputs
    
    image[coord] = color
    
    delta = 1 if delta else -1
    direction = (direction + delta) % 4
    dxdy = dxdy_dict[direction]
    x = coord[0] + dxdy[0]
    y = coord[1] + dxdy[1]
    coord = (x, y)
    inputs = [image[coord]]

xs = [coord[0] for coord in image]
ys = [coord[1] for coord in image]

xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)
dx = xmax - xmin
dy = ymax - ymin

image_str = '\n'.join([''.join(['#' if image[(x, y)] else ' ' for x in range(xmin-2, xmax+2)]) for y in range(ymax+2, ymin-2, -1)])
print(image_str)