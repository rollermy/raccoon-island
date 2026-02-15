#!/usr/bin/env python3
"""Generate an 80x80 Raccoon Island TMX map with concentric ring design.

Uses three tilesheets:
  1. spring_outdoorsTileSheet (grass, water, forest canopy, cobblestone)
  2. spring_beach (sand tiles)
  3. spring_town (building facades)

Zones (from center outward):
  - Town center (dist <= 14): Grass, paths, plaza, buildings
  - Forest ring (14 < dist <= 22): Dense varied tree canopy
  - Beach ring (22 < dist <= 27): Sandy beach ground
  - Water border (dist > 27): Deep ocean with Water property
"""

import math

WIDTH = 80
HEIGHT = 80
CX, CY = 40, 40

# === Tilesheet 1: spring_outdoorsTileSheet ===
# 400x1264, 25 cols x 79 rows, firstgid=1
OUT_FIRSTGID = 1
OUT_COLS = 25

WATER = 1275      # row 50, col 24 — uniform dark blue RGB(58,125,149)
GRASS = 176       # row 7, col 0  — bright green RGB(74,164,29)
COBBLE = 979      # row 39, col 3 — gray stone RGB(141,145,148)

# (Trees are now spawned as TerrainFeature objects in ModEntry.cs)

# === Tilesheet 2: spring_beach ===
# 272x496, 17 cols x 31 rows, firstgid=1976
BEACH_FIRSTGID = 1976
BEACH_COLS = 17

def beach_gid(row, col):
    return BEACH_FIRSTGID + row * BEACH_COLS + col

# Shallow turquoise water — row 3, cols 6-8
SHALLOW_WATER = [beach_gid(3, c) for c in range(6, 9)]
# Ocean water from beach sheet (rows 0-1, cols 7-9 mid-blue; cols 10-11 deep blue)
OCEAN_MID = [beach_gid(r, c) for r in range(2) for c in range(7, 10)]
OCEAN_DEEP = [beach_gid(r, c) for r in range(2) for c in range(10, 12)]
# All ocean tiles get the Water property (game draws animated water overlay on these)
BEACH_WATER_TILE_IDS = sorted(set(
    [gid - BEACH_FIRSTGID for gid in OCEAN_MID + OCEAN_DEEP]
))

# === Tilesheet 5: island_tilesheet_1 ===
# 512x1040, 32 cols x 65 rows (base non-seasonal island tilesheet)
ISLAND_FIRSTGID = 4816
ISLAND_COLS = 32

def island_gid(row, col):
    return ISLAND_FIRSTGID + row * ISLAND_COLS + col

# Tropical ocean tiles — row 0, cols 0-15 (turquoise/teal, semi-transparent)
# These overlay on top of a solid dark teal base
ISLAND_OCEAN = [island_gid(0, c) for c in range(16)]
# Tile IDs within the island tilesheet that should have Water property
ISLAND_WATER_TILE_IDS = list(range(16))  # row 0, cols 0-15

# Wooden dock plank tiles — from island tilesheet row 17 (Ginger Island pier planks)
DOCK_PLANKS = [island_gid(17, c) for c in range(5, 9)]

# Dry sand — from island tilesheet (flat tropical sand tiles)
DRY_SAND = [
    island_gid(1, 5), island_gid(1, 6), island_gid(1, 8),  # light sand
    island_gid(2, 1), island_gid(2, 7), island_gid(2, 8),  # light sand variants
    island_gid(3, 7), island_gid(3, 8),                     # slightly darker sand
    island_gid(4, 1), island_gid(4, 2), island_gid(4, 3),  # more variants
]

# === Tilesheet 3: spring_town ===
# 512x1152, 32 cols x 72 rows, firstgid=2503
TOWN_FIRSTGID = 2503
TOWN_COLS = 32


def town_gid(row, col):
    return TOWN_FIRSTGID + row * TOWN_COLS + col



# === Zone thresholds ===
WATER_MIN = 27
BEACH_MIN = 22
FOREST_MIN = 14


def get_dist(x, y):
    return math.sqrt((x - CX) ** 2 + (y - CY) ** 2)


def get_zone(x, y):
    dist = get_dist(x, y)
    if dist > WATER_MIN:
        return "water"
    elif dist > BEACH_MIN:
        return "beach"
    elif dist > FOREST_MIN:
        return "forest"
    else:
        return "town"


def is_ns_path(x, y):
    return x in (39, 40) and get_zone(x, y) == "forest"


def is_ew_path(x, y):
    return y in (39, 40) and get_zone(x, y) == "forest"


def is_dock(x, y):
    """Small south-facing pier like Ginger Island — 2 tiles wide, extends from beach into water."""
    if x not in (39, 40):
        return False
    return 65 <= y <= 70


def is_plaza(x, y):
    return abs(x - CX) <= 3 and abs(y - CY) <= 3 and get_zone(x, y) == "town"


def is_town_path(x, y):
    if get_zone(x, y) != "town":
        return False
    return x in (39, 40) or y in (39, 40)




def dock_tile(x, y):
    """Pick a wooden dock plank tile."""
    h = (x * 7 + y * 13) % 100
    return DOCK_PLANKS[h % len(DOCK_PLANKS)]


def ocean_tile(x, y):
    """Pick a tropical island ocean tile."""
    h = (x * 7 + y * 13) % 100
    return ISLAND_OCEAN[h % len(ISLAND_OCEAN)]


def beach_tile(x, y):
    """Pick a dry sand beach tile."""
    h = (x * 7 + y * 13) % 100  # deterministic variation
    return DRY_SAND[h % len(DRY_SAND)]


# === Building definitions ===
# Each building: (map_x, map_y, width, height, name)
# Buildings layer gets wall tiles, Front layer gets roof tiles
# Door at bottom-center (1 tile gap in Buildings layer)

BUILDINGS = []

# Cobblestone pads where PermanentTent LargeTerrainFeatures are placed.
# Tent Tile is center; bounding box is (Tile.X-1, Tile.Y-1) size 3x2.
# 12 tents in an even ring (radius ~11, 30° apart, starting at 15° to avoid paths)
TENT_PADS = [
    {"x": 50, "y": 36, "w": 3, "h": 2},  # Tent01 Tile(51,37) — E, above path
    {"x": 47, "y": 31, "w": 3, "h": 2},  # Tent02 Tile(48,32) — NE
    {"x": 42, "y": 28, "w": 3, "h": 2},  # Tent03 Tile(43,29) — N, right of path
    {"x": 35, "y": 28, "w": 3, "h": 2},  # Tent04 Tile(36,29) — N, left of path
    {"x": 31, "y": 31, "w": 3, "h": 2},  # Tent05 Tile(32,32) — NW
    {"x": 28, "y": 36, "w": 3, "h": 2},  # Tent06 Tile(29,37) — W, above path
    {"x": 28, "y": 42, "w": 3, "h": 2},  # Tent07 Tile(29,43) — W, below path
    {"x": 31, "y": 47, "w": 3, "h": 2},  # Tent08 Tile(32,48) — SW
    {"x": 35, "y": 50, "w": 3, "h": 2},  # Tent09 Tile(36,51) — S, left of path
    {"x": 42, "y": 50, "w": 3, "h": 2},  # Tent10 Tile(43,51) — S, right of path
    {"x": 47, "y": 47, "w": 3, "h": 2},  # Tent11 Tile(48,48) — SE
    {"x": 50, "y": 42, "w": 3, "h": 2},  # Tent12 Tile(51,43) — E, below path
]

# Well at center-north of plaza
WELL = {"x": 42, "y": 37, "w": 2, "h": 2}


def get_building_tiles():
    """Pre-compute building tile positions."""
    building_cells = {}  # (x, y) -> {"back": gid, "buildings": gid, "front": gid}

    for b in BUILDINGS:
        bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
        door_x = bx + bw // 2

        for dy in range(bh):
            for dx in range(bw):
                mx, my = bx + dx, by + dy
                cell = {"back": COBBLE, "buildings": 0, "front": 0}

                if dy < 2:
                    cell["front"] = town_gid(dy, dx % 5)
                is_door = (dy == bh - 1 and mx == door_x)
                if not is_door:
                    cell["buildings"] = town_gid(6 + dy, dx % 5)

                building_cells[(mx, my)] = cell

    # Tent pads: cobblestone ground only (tent sprite drawn by PermanentTent)
    for pad in TENT_PADS:
        for dy in range(pad["h"]):
            for dx in range(pad["w"]):
                mx, my = pad["x"] + dx, pad["y"] + dy
                building_cells[(mx, my)] = {"back": COBBLE, "buildings": 0, "front": 0}

    # Well
    wx, wy = WELL["x"], WELL["y"]
    for dy in range(WELL["h"]):
        for dx in range(WELL["w"]):
            mx, my = wx + dx, wy + dy
            building_cells[(mx, my)] = {
                "back": COBBLE,
                "buildings": COBBLE,  # stone well blocks movement
                "front": 0,
            }

    return building_cells


def generate_layers():
    building_cells = get_building_tiles()
    back = []
    buildings = []
    front = []

    for y in range(HEIGHT):
        back_row = []
        buildings_row = []
        front_row = []

        for x in range(WIDTH):
            zone = get_zone(x, y)
            on_path = is_ns_path(x, y) or is_ew_path(x, y)
            on_dock = is_dock(x, y)
            on_plaza = is_plaza(x, y)
            on_town_path = is_town_path(x, y)
            in_building = (x, y) in building_cells

            # Back layer
            if in_building:
                back_row.append(building_cells[(x, y)]["back"])
            elif on_dock:
                back_row.append(dock_tile(x, y))
            elif zone == "water":
                back_row.append(ocean_tile(x, y))
            elif zone == "beach":
                back_row.append(beach_tile(x, y))
            elif zone == "forest":
                back_row.append(COBBLE if on_path else GRASS)
            else:  # town
                if on_plaza or on_town_path:
                    back_row.append(COBBLE)
                else:
                    back_row.append(GRASS)

            # Buildings layer — block movement in deep water and dock edges
            dock_edge = (
                zone == "water" and not on_dock
                and x in (38, 41) and 65 <= y <= 70
            )
            if in_building:
                buildings_row.append(building_cells[(x, y)]["buildings"])
            elif on_dock:
                buildings_row.append(0)
            elif dock_edge or (zone == "water" and get_dist(x, y) > 32):
                buildings_row.append(ocean_tile(x, y))
            else:
                buildings_row.append(0)

            # Front layer
            if in_building:
                front_row.append(building_cells[(x, y)]["front"])
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

    # Build Water property entries for beach ocean tiles
    beach_water_props = "\n".join(
        f'  <tile id="{tid}">\n'
        f'   <properties>\n'
        f'    <property name="Water" value="T"/>\n'
        f'   </properties>\n'
        f'  </tile>'
        for tid in BEACH_WATER_TILE_IDS
    )

    # Build Water property entries for island ocean tiles
    island_water_props = "\n".join(
        f'  <tile id="{tid}">\n'
        f'   <properties>\n'
        f'    <property name="Water" value="T"/>\n'
        f'   </properties>\n'
        f'  </tile>'
        for tid in ISLAND_WATER_TILE_IDS
    )

    tmx = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.11.0" orientation="orthogonal" renderorder="right-down" width="{WIDTH}" height="{HEIGHT}" tilewidth="16" tileheight="16" infinite="0" nextlayerid="4" nextobjectid="1">
 <tileset firstgid="{OUT_FIRSTGID}" name="outdoors" tilewidth="16" tileheight="16" tilecount="1975" columns="25">
  <image source="Maps/spring_outdoorsTileSheet.png" width="400" height="1264"/>
 </tileset>
 <tileset firstgid="{BEACH_FIRSTGID}" name="z_beach" tilewidth="16" tileheight="16" tilecount="527" columns="17">
  <image source="Maps/spring_beach.png" width="272" height="496"/>
{beach_water_props}
 </tileset>
 <tileset firstgid="{TOWN_FIRSTGID}" name="z_town" tilewidth="16" tileheight="16" tilecount="2304" columns="32">
  <image source="Maps/spring_town.png" width="512" height="1152"/>
 </tileset>
 <tileset firstgid="{ISLAND_FIRSTGID}" name="z_island" tilewidth="16" tileheight="16" tilecount="2080" columns="32">
  <image source="Maps/island_tilesheet_1.png" width="512" height="1040"/>
{island_water_props}
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
    output_path = "assets/RaccoonIsland.tmx"
    with open(output_path, "w") as f:
        f.write(tmx_content)
    print(f"Generated {output_path} ({WIDTH}x{HEIGHT})")

    counts = {"water": 0, "beach": 0, "forest": 0, "town": 0}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            counts[get_zone(x, y)] += 1
    print(f"Zone stats: {counts}")

    building_count = sum(1 for b in BUILDINGS for dy in range(b["h"]) for dx in range(b["w"]))
    print(f"Building tiles: {building_count + WELL['w'] * WELL['h']}")
    print("Forest trees: spawned as TerrainFeature objects in ModEntry.cs")
