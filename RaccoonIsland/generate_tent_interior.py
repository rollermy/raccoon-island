"""Generate 8x6 tent interior TMX maps for RaccoonIsland mod.

Creates TentInteriorNW.tmx and TentInteriorNE.tmx using Maps/townInterior.png
(32 cols x 68 rows tilesheet from base game content).

Layout:
  - Back layer: wood floor tiles inside, void (0) outside
  - Buildings layer: wall tiles on perimeter blocking movement, gap at bottom-center for exit
  - Front layer: upper wall decoration for depth

Exit warp tiles at (3,5) and (4,5) — bottom-center of the map.
"""

# townInterior.png: 512x1088, 32 cols x 68 rows
TI_FIRSTGID = 1
TI_COLS = 32

def ti_gid(row, col):
    return TI_FIRSTGID + row * TI_COLS + col

# Tile selections from townInterior.png
WOOD_FLOOR = ti_gid(20, 0)    # wood plank floor
WALL_TILE = ti_gid(0, 0)      # interior wall
WALL_TOP = ti_gid(1, 0)       # upper wall decoration (Front layer, depth)
VOID = 0

# Nest tilesheet (128x64 = 8 cols x 4 rows of 16x16 tiles)
NEST_FIRSTGID = TI_FIRSTGID + 2176  # after all townInterior tiles
NEST_COLS = 8
NEST_ROWS = 4
def nest_gid(row, col):
    return NEST_FIRSTGID + row * NEST_COLS + col

WIDTH = 10
HEIGHT = 12


def generate_layers():
    back = []
    buildings = []
    front = []

    for y in range(HEIGHT):
        back_row = []
        buildings_row = []
        front_row = []

        for x in range(WIDTH):
            is_perimeter = (x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1)
            is_exit = (y == HEIGHT - 1 and x in (3, 4))
            # Back layer: floor everywhere
            back_row.append(WOOD_FLOOR)

            # Buildings layer: walls on perimeter, gap at exit
            if is_perimeter and not is_exit:
                buildings_row.append(WALL_TILE)
            else:
                buildings_row.append(VOID)

            # Front layer: upper wall decoration on top row for depth
            if y == 0 and not (x == 0 or x == WIDTH - 1):
                front_row.append(WALL_TOP)
            else:
                front_row.append(VOID)

        back.append(back_row)
        buildings.append(buildings_row)
        front.append(front_row)

    return back, buildings, front


def layer_to_csv(layer):
    lines = []
    for i, row in enumerate(layer):
        line = ",".join(str(t) for t in row)
        if i < len(layer) - 1:
            line += ","
        lines.append(line)
    return "\n".join(lines)


def generate_tmx(name):
    back, buildings, front = generate_layers()

    tmx = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.11.0" orientation="orthogonal" renderorder="right-down" width="{WIDTH}" height="{HEIGHT}" tilewidth="16" tileheight="16" infinite="0" nextlayerid="4" nextobjectid="1">
 <tileset firstgid="{TI_FIRSTGID}" name="townInterior" tilewidth="16" tileheight="16" tilecount="2176" columns="32">
  <image source="Maps/townInterior.png" width="512" height="1088"/>
 </tileset>
 <tileset firstgid="{NEST_FIRSTGID}" name="nest" tilewidth="16" tileheight="16" tilecount="{NEST_COLS * NEST_ROWS}" columns="{NEST_COLS}">
  <image source="nest_tiles.png" width="{NEST_COLS * 16}" height="{NEST_ROWS * 16}"/>
 </tileset>
 <layer id="1" name="Back" width="{WIDTH}" height="{HEIGHT}">
  <data encoding="csv">
{layer_to_csv(back)}
</data>
 </layer>
 <layer id="2" name="Buildings" width="{WIDTH}" height="{HEIGHT}">
  <data encoding="csv">
{layer_to_csv(buildings)}
</data>
 </layer>
 <layer id="3" name="Front" width="{WIDTH}" height="{HEIGHT}">
  <data encoding="csv">
{layer_to_csv(front)}
</data>
 </layer>
</map>
'''
    return tmx


if __name__ == "__main__":
    for i in range(1, 13):
        name = f"TentInterior{i:02d}"
        tmx_content = generate_tmx(name)
        output_path = f"assets/{name}.tmx"
        with open(output_path, "w") as f:
            f.write(tmx_content)
        print(f"Generated {output_path} ({WIDTH}x{HEIGHT})")
