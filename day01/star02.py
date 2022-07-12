def fuel(mass):
    return max(0, mass//3 - 2)

def total_fuel(mass):
    mass = fuel(mass)
    total = mass
    while mass:
        mass = fuel(mass)
        total += mass
    return total

total = sum([total_fuel(int(mass)) for mass in open('input.txt')])

print(f"{total = }")

