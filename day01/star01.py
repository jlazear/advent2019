def fuel(mass):
    return mass//3 - 2

total = sum([fuel(int(mass)) for mass in open('input.txt')])
print(f"{total = }")