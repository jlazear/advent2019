import numpy as np

def parse_input(fname='input.txt'):
    with open(fname) as f:
        s = f.read().strip()
    arr = np.array([c for c in s], dtype='int')
    return arr

arr = parse_input()

nx, ny = 25, 6
arr = arr.reshape(-1, ny, nx)

n_zeros = np.sum(arr == 0, axis=(1, 2))
argmin_zeros = np.argmin(n_zeros)
n_ones = np.sum(arr[argmin_zeros] == 1)
n_twos = np.sum(arr[argmin_zeros] == 2)
print(f"{n_ones*n_twos = }")