def parse_input(fname='input.txt'):
    with open(fname) as f:
        wire1 = [(x[0], int(x[1:])) for x in f.readline().strip().split(',')]
        wire2 = [(x[0], int(x[1:])) for x in f.readline().strip().split(',')]
    return wire1, wire2


def make_wire(wire, record=None):
    if record is None:
        record = set()
    pos = (0, 0)
    for cmd, distance in wire:
        for _ in range(distance):
            if cmd == 'R':
                pos = (pos[0] + 1, pos[1])
            elif cmd == 'L':
                pos = (pos[0] - 1, pos[1])                
            elif cmd == 'U':
                pos = (pos[0], pos[1] + 1)                
            elif cmd == 'D':
                pos = (pos[0], pos[1] - 1)                
            record.add(pos)
    return record

def mandist(coord):
    return abs(coord[0]) + abs(coord[1])
    
def min_dist(fname='input.txt'):
    wire1, wire2 = parse_input(fname)
    record1 = make_wire(wire1)
    record2 = make_wire(wire2)
    intersections = record1 & record2
    return min(map(mandist, intersections))

for fname in ['test0.txt', 'test1.txt', 'test2.txt', 'input.txt']:
    print(f"{fname} {min_dist(fname) = }")