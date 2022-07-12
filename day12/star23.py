from dataclasses import dataclass
from itertools import combinations
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

    def __str__(self):
        rs = ','.join([str(x) for x in self.r])
        vs = ','.join([str(x) for x in self.v])
        return f"P(({rs}), ({vs}), {self.PE()}*{self.KE()}={self.energy()})"

    def __repr__(self):
        return self.__str__()


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

def update(planets):
    pairs = combinations(planets, 2)
    for pair in pairs:
        p1, p2 = pair
        p1.update_velocity(p2)
    
    for planet in planets:
        planet.update_position()

def total_energy(planets):
    return sum([planet.energy() for planet in planets])

planets = parse_input('input.txt')
for i in range(1000):
    update(planets)

total_energy = sum([planet.energy() for planet in planets])
print(f"{total_energy = }")