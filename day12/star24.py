from dataclasses import dataclass
from itertools import combinations
from math import lcm
import numpy as np

@dataclass
class Planet:
    r: np.ndarray
    v: np.ndarray

    def update_velocity(self, other):
        dr = self.r - other.r
        dv = np.sign(dr)
        
        other.v += dv
        self.v -= dv

    def update_position(self):
        self.r += self.v

    def energy(self):
        return np.sum(np.abs(self.r)) * np.sum(np.abs(self.v))

    def hash_planet(self, axis):
        return (self.r[axis], self.v[axis])


def parse_input(fname='input.txt'):
    with open(fname) as f:
        planets = []
        for line in f:
            xstr, ystr, zstr = line.strip().split(', ')
            x = int(xstr.strip('<>').split('=')[1])
            y = int(ystr.split('=')[1])
            z = int(zstr.strip('<>').split('=')[1])
            planet = Planet(np.array([x, y, z]), np.array([0, 0, 0]))
            planets.append(planet)
    return planets

def hash_planets(planets, axis):
    return tuple(planet.hash_planet(axis) for planet in planets)

def update(planets):  # could add axis-specific updates and stop updating once cycle found, but meh
    pairs = combinations(planets, 2)
    for pair in pairs:
        p1, p2 = pair
        p1.update_velocity(p2)
    
    for planet in planets:
        planet.update_position()

planets = parse_input('input.txt')
planets_hash_x0 = hash_planets(planets, 0)
planets_hash_y0 = hash_planets(planets, 1)
planets_hash_z0 = hash_planets(planets, 2)
nx = ny = nz = None
i = 0
while not (nx and ny and nz):
    update(planets)
    i += 1

    if not nx and (hash_planets(planets, 0) == planets_hash_x0):
        nx = i
        # print(f"found nx at {i}")  #DELME
    if not ny and (hash_planets(planets, 1) == planets_hash_y0): 
        ny = i
        # print(f"found ny at {i}")  #DELME        
    if not nz and (hash_planets(planets, 2) == planets_hash_z0): 
        nz = i
        # print(f"found nz at {i}")  #DELME        


print(f"x repeats after {nx} steps")
print(f"y repeats after {ny} steps")
print(f"z repeats after {nz} steps")
print(f"xyz repeats after {lcm(nx, ny, nz) = } steps")
