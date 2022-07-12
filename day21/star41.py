import intcode

program = intcode.parse_input('input.txt')

inputs = None
outputs = None
pos = None
base = None
halt = False
waiting = False

while not waiting:
    outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, pos=pos, base=base, outputs=outputs)

springscript = (
"""NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
""")
inputs = [ord(c) for c in springscript]

while not halt:
    outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, pos=pos, base=base, outputs=outputs)

response = ''.join([chr(c) for c in outputs if c < 0x110000])
print(response)
if outputs[-1] >= 0x110000:
    print(f"damage = {outputs[-1]}")

# when jumps, lands 4 tiles away
# so jump any time (~A | ~B | ~C) & D = (~A + ~B + ~C)D