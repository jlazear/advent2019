from collections import deque
from functools import cache
import numpy as np

def make_number(n):
    return deque([int(c) for c in str(n)])

def fft_end(n):
    if not isinstance(n, deque):
        n = make_number(n)
    n2 = deque([n.pop()])
    while n:
        c = n.pop()
        n2.appendleft(c + n2[0])

    n2 = deque([abs(x) % 10 for x in n2])
    return n2

def find_message(n):
    offset = int(n[:7])
    subn = (10000*n)[offset:]

    for i in range(100):
        print(f"{i = }")
        subn = fft_end(subn)

    message = int(''.join([str(subn.popleft()) for _ in range(8)]))
    return message

n = open('input.txt').read().strip()
message = find_message(n)
print(f"{message = }")
