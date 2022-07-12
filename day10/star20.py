from collections import defaultdict
from math import gcd, atan2, pi

def parse_input(fname='input.txt'):
    asteroids = set()
    with open(fname) as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.strip()):
                if c == '#':
                    asteroids.add((j, i))
    return asteroids

def map_asteroids(coord, asteroids):
    counter = defaultdict(list)
    for coord2 in asteroids:
        if coord == coord2:
            continue
        dx = coord2[0] - coord[0]
        dy = coord2[1] - coord[1]
        divisor = gcd(dx, dy)
        counter[(dx//divisor, dy//divisor)].append(coord2)
    return counter

def sort_asteroid_map(coord, asteroid_map):
    new_map = defaultdict(list)
    for angle, asteroids in asteroid_map.items():
        distances = [(coord2[0] - coord[0])**2 + (coord2[1] - coord[1])**2 for coord2 in asteroids]
        sorted_distances_asteroids = sorted(zip(distances, asteroids))
        sorted_asteroids = [t[1] for t in sorted_distances_asteroids]
        new_map[angle] = sorted_asteroids
    return new_map

asteroids = parse_input('input.txt')

num = 0
asteroid_map = None
best_coord = None
for coord in asteroids:
    amap = map_asteroids(coord, asteroids)
    new_num = len(amap)
    if new_num > num:
        asteroid_map = amap
        num = new_num
        best_coord = coord

print(f"{best_coord = }")

asteroid_map = sort_asteroid_map(best_coord, asteroid_map)

angles = map(lambda x: atan2(x[1], x[0]), [coord for coord in asteroid_map.keys()])
# angle = 0 corresponds to +x (=+i), and increasing angle corresponds to clockwise in xy (since +j -> -y)
# so need to shift by 270 deg = 3pi/2 to get to pointing +y = -j
angles = [(angle - 3*pi/2)*180/pi % 360 for angle in angles]

sorted_coords = sorted(zip(angles, list(asteroid_map.keys())), reverse=False)

n_destroyed = 0
angles_index = 0
max_angles_index = len(angles)
while n_destroyed < 200:
    angle, coord = sorted_coords[angles_index]
    if len(asteroid_map[coord]):
        n_destroyed += 1
        destroying = asteroid_map[coord].pop(0)
        # print(f"{n_destroyed = }, {destroying = }, {coord = }, {angle = }")
    angles_index = (angles_index + 1) % max_angles_index  # increasing angle -> clockwise in xy since +j -> -y

answer = 100*destroying[0] + destroying[1]
print(f"{destroying = }, {answer = }")
