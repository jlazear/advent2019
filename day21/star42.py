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

# when jumps, lands 4 tiles away (at D)
# so jump if any of the nearest 3 tiles (A, B, C) are empty and 4 away (D) is available
# must also either be able to jump or take a step forward after landing, so need either E or H to also be available
# so jump any time (~A | ~B | ~C) & D & (H | E)= (~A + ~B + ~C)(H + E)D
# reload temporary variable with a particular input using Y = NOT NOT X
# which gives Y = X, independent of previous value of Y

springscript = (
"""NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
AND D J
RUN
""")

inputs = [ord(c) for c in springscript]

while not halt:
    outputs, halt, waiting, new_out, pos, base, inpos = intcode.intcode(program, inputs=inputs, pos=pos, base=base, outputs=outputs)

response = ''.join([chr(c) for c in outputs if c < 0x110000])
print(response)
if outputs[-1] >= 0x110000:
    print(f"damage = {outputs[-1]}")

