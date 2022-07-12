def check_valid(password, minval, maxval):
    in_range = (minval <= password <= maxval)
    increasing = True
    repeated = False
    password = str(password)
    for i in range(1, len(password)):
        if password[i-1] == password[i]:
            repeated = True
        if password[i-1] > password[i]:
            increasing = False
    return in_range and increasing and repeated

minval, maxval = (int(x) for x in open('input.txt').read().split('-'))

count = 0
for password in range(minval, maxval+1):
    if check_valid(password, minval, maxval):
        count += 1

print(f"{count = }")

