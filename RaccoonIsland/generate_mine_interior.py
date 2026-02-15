"""Generate a 16x12 mine interior TMX map for RaccoonIsland mod.

Uses Maps/townInterior.png tilesheet (32 cols x 68 rows).
Exit warp tiles at (7,11) and (8,11) — bottom-center.
"""

TI_FIRSTGID = 1
TI_COLS = 32

def ti_gid(row, col):
    return TI_FIRSTGID + row * TI_COLS + col

STONE_FLOOR = ti_gid(22, 0)   # dark stone floor
WALL_TILE = ti_gid(0, 0)      # interior wall
WALL_TOP = ti_gid(1, 0)       # upper wall decoration

WIDTH = 16
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
            is_exit = (y == HEIGHT - 1 and x in (7, 8))

            back_row.append(STONE_FLOOR)

            if is_perimeter and not is_exit:
                buildings_row.append(WALL_TILE)
            else:
                buildings_row.append(0)

            if y == 0 and 0 < x < WIDTH - 1:
                front_row.append(WALL_TOP)
            else:
                front_row.append(0)

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


def generate_tmx():
    back, buildings, front = generate_layers()

    tmx = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.11.0" orientation="orthogonal" renderorder="right-down" width="{WIDTH}" height="{HEIGHT}" tilewidth="16" tileheight="16" infinite="0" nextlayerid="4" nextobjectid="1">
 <tileset firstgid="{TI_FIRSTGID}" name="townInterior" tilewidth="16" tileheight="16" tilecount="2176" columns="32">
  <image source="Maps/townInterior.png" width="512" height="1088"/>
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
    tmx_content = generate_tmx()
    output_path = "assets/RaccoonMine.tmx"
    with open(output_path, "w") as f:
        f.write(tmx_content)
    print(f"Generated {output_path} ({WIDTH}x{HEIGHT})")
