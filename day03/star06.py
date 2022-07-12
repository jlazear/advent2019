import sys
from collections import defaultdict

def parse_input(fname='input.txt'):
    with open(fname) as f:
        wire1 = [(x[0], int(x[1:])) for x in f.readline().strip().split(',')]
        wire2 = [(x[0], int(x[1:])) for x in f.readline().strip().split(',')]
    return wire1, wire2


def make_wire(wire, record=None):
    if record is None:
        record = defaultdict(lambda: sys.maxsize)
    pos = (0, 0)
    steps = 0
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
            steps += 1
            record[pos] = min(record[pos], steps)
    return record

def min_steps(fname='input.txt'):
    wire1, wire2 = parse_input(fname)
    record1 = make_wire(wire1)
    record2 = make_wire(wire2)
    intersections = set(record1.keys()) & set(record2.keys())
    steps = {coord: record1[coord] + record2[coord] for coord in intersections}
    return min(steps.values())




for fname in ['test0.txt', 'test1.txt', 'test2.txt', 'input.txt']:
    print(f"{fname} {min_steps(fname) = }")