from functools import cache

def parse_input(fname='input.txt'):
    commands = []
    for line in open(fname):
        if line.startswith('deal with'):
            elements = line.split()
            arg = int(elements[-1])
            commands.append(('dwi', arg))
        elif line.startswith('deal into'):
            commands.append(('dins', 0))
        else:  # cut
            elements = line.split()
            arg = int(elements[-1])
            commands.append(('cut', arg))
    return commands

def make_deck(stack, ncards=10007):
    """stack = (p0, delta) tracks position of card 0 and offset to card 1
    
    card n will be found at position (p0 + n*delta) mod ncards
    """
    pos, increment = stack
    deck = [None]*ncards
    for i in range(ncards):
        deck[(pos + i*increment) % ncards] = i
    return deck

def deal_into_new_stack(stack, *arg, ncards=10007):
    pos, increment = stack
    pos = ncards - pos - 1
    increment = -increment % ncards
    return (pos, increment)

def cut(stack, arg, ncards=10007):
    pos, increment = stack
    pos = (pos - arg) % ncards
    return (pos, increment)

def deal_with_increment(stack, arg, ncards=10007):
    pos, increment = stack
    pos = (pos * arg) % ncards
    increment = (increment*arg) % ncards
    return (pos, increment)

cmd_dict = {'dwi': deal_with_increment,
            'dins': deal_into_new_stack,
            'cut': cut}
def command(stack, cmd, arg, ncards=10007, cmd_dict=cmd_dict):
    return cmd_dict[cmd](stack, arg, ncards=ncards)

def shuffle(fname='input.txt', ncards=10007, stack=(0, 1)):
    commands = parse_input(fname)
    stack = stack
    for cmd, arg in commands:
        stack = command(stack, cmd, arg, ncards=ncards)
    return stack

@cache
def F(beta, n, m):
    """Recursively computes sum_{i=0}^n beta^i mod m"""
    if n == 0: 
        return 1
    elif n < 0:
        return 0
    elif n % 2:  # odd
        return ((1 + beta)*F((beta*beta) % m, (n-1)//2, m)) % m
    else:  # even
        return (1 + ((beta + beta*beta) % m)*F((beta*beta) % m, n//2 - 1, m)) % m

def shuffleN(fname='input.txt', ncards=10007, nshuffles=10, stack=(0, 1)):
    alpha, beta = shuffle(fname, ncards=ncards, stack=stack)
    p = (alpha*F(beta, nshuffles-1, ncards)) % ncards
    delta = pow(beta, nshuffles, ncards)
    return (p, delta)

def get_card(pos, stack, ncards):
    """Solves modular arithmetic equation (p0 + i*delta) mod ncards = pos
    
    i.e. i = delta^-1 * (pos - p0) mod ncards
    using Euler's formula
       delta^-1 mod m = delta^(m-2) mod m
    if m is prime
    """
    p0, delta = stack
    i = (pow(delta, ncards-2, ncards) * (pos - p0)) % ncards
    return i

ncards = 119315717514047
nshuffles = 101741582076661

stack = shuffleN(fname='input.txt', ncards=ncards, nshuffles=nshuffles)

print(f"{get_card(2020, stack, ncards) = }")