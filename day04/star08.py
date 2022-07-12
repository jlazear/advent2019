def check_valid(password, minval, maxval):
    in_range = (minval <= password <= maxval)
    increasing = True
    repeated = False
    password = str(password)
    match_len = 0
    c = password[0]
    for i in range(1, len(password)):
        next_c = password[i]
        if c == next_c:
            match_len += 1
        else:
            if match_len == 1:
                repeated = True
            match_len = 0
        
        if c > next_c:
            increasing = False
        c = next_c            
    if match_len == 1:
        repeated = True
    return in_range and increasing and repeated

minval, maxval = (int(x) for x in open('input.txt').read().split('-'))

count = 0
for password in range(minval, maxval+1):
    if check_valid(password, minval, maxval):
        count += 1

print(f"{count = }")

