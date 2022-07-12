def make_number(n):
    return [int(c) for c in str(n)]

def get_pattern(i, position, base=(0, 1, 0, -1)):
    i_base = ((i+1) // (position+1)) % 4
    return base[i_base]

def get_element(number, position):
    return abs(sum(number[i] * get_pattern(i, position) for i in range(len(number)))) % 10

def fft(n):
    if isinstance(n, int):
        n = make_number(n)
    return [get_element(n, pos) for pos in range(len(n))]

n = int(open('input.txt').read())

for i in range(100):
    n = fft(n)

first8 = int(''.join([str(x) for x in n[:8]]))
print(f"{first8 = }")