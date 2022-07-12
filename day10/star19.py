from collections import Counter
from math import gcd

def parse_input(fname='input.txt'):
    asteroids = set()
    with open(fname) as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.strip()):
                if c == '#':
                    asteroids.add((i, j))
    return asteroids

def map_asteroids(coord, asteroids):
    counter = Counter()
    for coord2 in asteroids:
        if coord == coord2:
            continue
        dx = coord2[0] - coord[0]
        dy = coord2[1] - coord[1]
        divisor = gcd(dx, dy)
        counter[(dx//divisor, dy//divisor)] += 1
    return len(counter)

asteroids = parse_input()

counts = [map_asteroids(coord, asteroids) for coord in asteroids]
print(f"{max(counts) = }")
