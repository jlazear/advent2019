import intcode

program = intcode.parse_input('input.txt')

outputs, halt, waiting, pos, base = intcode.intcode(program)

tiles = {}
while outputs:
    tile_id = outputs.pop()
    y = outputs.pop()
    x = outputs.pop()
    tiles[(x, y)] = tile_id

print(f"{len([tile for tile, tile_id in tiles.items() if tile_id == 2]) = }")