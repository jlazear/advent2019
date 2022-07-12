from collections import defaultdict
import intcode

def print_room(room):
    d = {-1: '?',
          0: '█',
          1: '.',
          2: 'O',
          3: 'S'}
    xs = [coord[0] for coord in room]
    ys = [coord[1] for coord in room]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    s = '\n'.join([''.join(['O' if (x, y) == 0 else d[room[(x, y)] ] for x in range(xmin-2, xmax+2)]) for y in range(ymin-2, ymax+2)])
    return s

def explore_room(program):
    turn_right = {1: 4, 4: 2, 2: 3, 3: 1}  # north (1), south (2), west (3), and east (4)
    turn_left = {value: key for key, value in turn_right.items()}  # north (1), south (2), west (3), and east (4)
    delta = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
    coord = (0, 0)
    room = defaultdict(lambda: -1)
    room[coord] = 1
    direction = 1  # start north
    seen = defaultdict(list)
    prev = 1

    tiles = None
    inputs = [direction]
    outputs = None
    pos = None
    base = None
    halt = False

    while not halt:
        # pick direction
        if prev:  # not wall
            right_direction = turn_right[direction]
            right_delta = delta[right_direction]
            coord_right = (coord[0] + right_delta[0], coord[1] + right_delta[1])
            right_val = room[coord_right]
            if right_val != 0:  # right is not a wall
                direction = right_direction
        else:  # wall
            direction = turn_left[direction]

        # stop if already explored this hallway from the same direction
        if direction in seen[coord]:
            break

        # move forward
        seen[coord].append(direction)
        inputs = [direction]
        outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, pos=pos, base=base)

        # store results
        code = outputs[0]
        # print(f"{i}: {coord} {direction} -> {code}")  #DELME
        coord2 = (coord[0] + delta[direction][0], coord[1] + delta[direction][1])
        if code == 0:
            room[coord2] = 0
        else:
            coord = coord2
            room[coord] = code
        prev = code

    room[(0, 0)] = 3
    return room

def dfs(room, start=(0, 0)):
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = [(0, start)]
    seen = set()
    depth = 0
    while queue:
        num, coord = queue.pop()
        depth = max(depth, num)
        seen.add(coord)
        adjacent_coords = [(coord[0] + delta[0], coord[1] + delta[1]) for delta in deltas]
        adjacent = [(num+1, coord2) for coord2 in adjacent_coords if room[coord2] != 0 and coord2 not in seen]
        queue.extend(adjacent)
    return depth


program = intcode.parse_input('input.txt')
room = explore_room(program)
# print(print_room(room))
for coord, value in room.items():
    if value == 2:
        start = coord
depth = dfs(room, start=start)
print(f"{depth = }")