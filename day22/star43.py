from collections import deque

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

def deal_into_new_stack(stack, *args):
    stack.reverse()
    return stack

def cut(stack, arg):
    if arg >= 0:
        for _ in range(arg):
            stack.append(stack.popleft())
    else:
        for _ in range(-arg):
            stack.appendleft(stack.pop())
    return stack

def deal_with_increment(stack, arg):
    newstack = [None]*len(stack)
    i = 0
    while stack:
        newstack[i] = stack.popleft()
        i = (i + arg) % len(newstack)
    return deque(newstack)

cmd_dict = {'dwi': deal_with_increment,
            'dins': deal_into_new_stack,
            'cut': cut}
def command(stack, cmd, arg, cmd_dict=cmd_dict):
    return cmd_dict[cmd](stack, arg)

def shuffle(fname='input.txt', ncards=10007):
    commands = parse_input(fname)
    stack = deque(range(ncards))
    for cmd, arg in commands:
        stack = command(stack, cmd, arg)
    return stack

stack = shuffle('input.txt', 10007)
istack = {card: pos for pos, card in enumerate(stack)}
print(f"{istack[2019] = } ")