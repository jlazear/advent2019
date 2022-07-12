import numpy as np

def parse_input(fname='input.txt'):
    with open(fname) as f:
        s = f.read().strip()
    arr = np.array([c for c in s], dtype='int')
    return arr

def generate_image(arr):
    image = np.zeros(arr.shape[1:]) + 2
    for n in range(arr.shape[0]):
        for i in range(arr.shape[1]):
            for j in range(arr.shape[2]):
                image_ij = image[i, j]
                arr_ij = arr[n, i, j]
                if image_ij == 2:
                    image[i, j] = arr_ij
    return image

arr = parse_input()

nx, ny = 25, 6
arr = arr.reshape(-1, ny, nx)
image = generate_image(arr)

image2 = '\n'.join([''.join(['#' if c else ' ' for c in row]) for row in image])
print(image2)