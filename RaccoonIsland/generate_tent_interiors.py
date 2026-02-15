#!/usr/bin/env python3
"""Generate tent interior TMX maps — exact copy of vanilla FarmHouse.xnb.

12x12 tile map with 3 tilesheets + nest_tiles, copied directly from
the extracted FarmHouse.xnb tile data.
"""

WIDTH = 12
HEIGHT = 12

# --- Tilesheet definitions (exact names from vanilla FarmHouse) ---

# indoor (townInterior): 32 cols x 66 rows
TI_FIRSTGID = 1
TI_TILES = 2176
TI_COLS = 32

# untitled tile sheet (farmhouse_tiles): 12 cols x 20 rows
FH_FIRSTGID = TI_FIRSTGID + TI_TILES  # 2177
FH_TILES = 240
FH_COLS = 12

# walls_and_floors: 16 cols x 32 rows
WF_FIRSTGID = FH_FIRSTGID + FH_TILES  # 2417
WF_TILES = 512
WF_COLS = 16

# nest_tiles: 3 cols x 2 rows
NEST_FIRSTGID = WF_FIRSTGID + WF_TILES  # 2929
NEST_COLS = 3
NEST_TILES = 6


def I(n): return TI_FIRSTGID + n   # indoor / townInterior
def F(n): return FH_FIRSTGID + n   # farmhouse_tiles
def W(n): return WF_FIRSTGID + n   # walls_and_floors
E = 0                               # empty (no tile)


# === Exact tile data from vanilla FarmHouse.xnb ===

BACK = [
    # Row 0
    [F(0),  F(0),   F(0),   F(0),   F(0),   F(0),   F(0),   F(0),   F(0),   F(0),   F(0),   F(0)],
    # Row 1
    [F(0),  W(0),   W(0),   W(0),   W(0),   W(0),   W(0),   W(0),   W(0),   W(0),   W(0),   F(0)],
    # Row 2
    [F(0),  W(16),  W(16),  W(16),  W(16),  W(16),  W(16),  W(16),  W(16),  W(16),  W(16),  F(0)],
    # Row 3
    [W(470),W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), F(64)],
    # Row 4
    [W(470),W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), F(64)],
    # Row 5
    [W(470),W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), F(64)],
    # Row 6
    [W(470),W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), F(64)],
    # Row 7
    [W(470),W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), F(64)],
    # Row 8
    [W(470),W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), F(64)],
    # Row 9
    [W(470),W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), F(64)],
    # Row 10
    [W(470),W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), W(336), W(337), F(64)],
    # Row 11
    [W(470),W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), W(352), W(353), F(64)],
]

BUILDINGS = [
    # Row 0
    [F(0),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  F(0)],
    # Row 1
    [I(9),  E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(23)],
    # Row 2
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(35)],
    # Row 3
    [I(64), W(32),  W(32),  W(32),  W(32),  W(32),  W(32),  W(32),  W(32),  W(32),  W(32),  F(47)],
    # Row 4
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(59)],
    # Row 5
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(71)],
    # Row 6
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(83)],
    # Row 7
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(95)],
    # Row 8
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(107)],
    # Row 9
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(119)],
    # Row 10
    [F(120),E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      F(131)],
    # Row 11: door at col 3
    [F(0),  F(0),   I(64),  E,      F(136), F(0),   F(0),   F(0),   F(0),   F(0),   F(0),   F(0)],
]

FRONT = [
    # Row 0
    [I(9),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(10),  I(11)],
    # Row 1
    [I(64), I(1426),I(1426),I(1426),I(1426),I(1426),I(1426),I(1426),I(1426),I(1426),I(1426),I(68)],
    # Row 2
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 3
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 4
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 5
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 6
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 7
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 8
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 9
    [I(64), E,      E,      E,      E,      E,      E,      E,      E,      E,      E,      I(68)],
    # Row 10
    [I(160),I(161), I(162), E,      I(163), I(165), I(165), I(165), I(165), I(165), I(166), I(167)],
    # Row 11
    [F(0),  F(0),   I(96),  I(165), I(130), F(0),   F(0),   F(0),   F(0),   F(0),   F(0),   F(0)],
]


def generate_interior(name):
    import copy
    back = copy.deepcopy(BACK)
    buildings = copy.deepcopy(BUILDINGS)
    front = copy.deepcopy(FRONT)

    # Place raccoon nest (3x2) on floor at upper-right of walkable area
    for dy in range(2):
        for dx in range(3):
            buildings[5 + dy][8 + dx] = NEST_FIRSTGID + dy * NEST_COLS + dx

    def csv(layer):
        lines = []
        for i, row in enumerate(layer):
            line = ",".join(str(t) for t in row)
            if i < len(layer) - 1:
                line += ","
            lines.append(line)
        return "\n".join(lines)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.11.0" orientation="orthogonal" renderorder="right-down" width="{WIDTH}" height="{HEIGHT}" tilewidth="16" tileheight="16" infinite="0" nextlayerid="4" nextobjectid="1">
 <tileset firstgid="{TI_FIRSTGID}" name="indoor" tilewidth="16" tileheight="16" tilecount="{TI_TILES}" columns="{TI_COLS}">
  <image source="Maps/townInterior" width="512" height="1088"/>
 </tileset>
 <tileset firstgid="{FH_FIRSTGID}" name="untitled tile sheet" tilewidth="16" tileheight="16" tilecount="{FH_TILES}" columns="{FH_COLS}">
  <image source="Maps/farmhouse_tiles" width="192" height="320"/>
 </tileset>
 <tileset firstgid="{WF_FIRSTGID}" name="walls_and_floors" tilewidth="16" tileheight="16" tilecount="{WF_TILES}" columns="{WF_COLS}">
  <image source="Maps/walls_and_floors" width="256" height="512"/>
 </tileset>
 <tileset firstgid="{NEST_FIRSTGID}" name="nest" tilewidth="16" tileheight="16" tilecount="{NEST_TILES}" columns="{NEST_COLS}">
  <image source="nest_tiles.png" width="48" height="32"/>
 </tileset>
 <layer id="1" name="Back" width="{WIDTH}" height="{HEIGHT}">
  <data encoding="csv">
{csv(back)}
</data>
 </layer>
 <layer id="2" name="Buildings" width="{WIDTH}" height="{HEIGHT}">
  <data encoding="csv">
{csv(buildings)}
</data>
 </layer>
 <layer id="3" name="Front" width="{WIDTH}" height="{HEIGHT}">
  <data encoding="csv">
{csv(front)}
</data>
 </layer>
</map>
'''


if __name__ == "__main__":
    for i in range(1, 13):
        name = f"TentInterior{i:02d}"
        content = generate_interior(name)
        path = f"assets/{name}.tmx"
        with open(path, "w") as f:
            f.write(content)
        print(f"Generated {path} ({WIDTH}x{HEIGHT})")
