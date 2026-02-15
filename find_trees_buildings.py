#!/usr/bin/env python3
"""Identify tree canopy tiles and building tiles."""
from PIL import Image
import os

ASSETS = "/Users/jd/code/stardewvalley/extracted_assets"


def tile_info(img, row, col, tile_size=16, cols=25):
    x0, y0 = col * tile_size, row * tile_size
    tile = img.crop((x0, y0, x0 + tile_size, y0 + tile_size))
    pixels = list(tile.getdata())
    opaque = [(r, g, b, a) for r, g, b, a in pixels if a > 128]
    if not opaque:
        return None
    avg_r = sum(r for r, g, b, a in opaque) // len(opaque)
    avg_g = sum(g for r, g, b, a in opaque) // len(opaque)
    avg_b = sum(b for r, g, b, a in opaque) // len(opaque)
    return (avg_r, avg_g, avg_b, len(opaque) / len(pixels))


# Outdoor tilesheet - find good tree canopy tiles (rows 0-3)
print("=== OUTDOOR SHEET: Tree canopy tiles (rows 0-3) ===")
img = Image.open(os.path.join(ASSETS, "spring_outdoorsTileSheet.png")).convert("RGBA")
out_cols = 25

for row in range(4):
    for col in range(out_cols):
        info = tile_info(img, row, col)
        if info:
            r, g, b, opacity = info
            gid = row * out_cols + col + 1
            if g > 80 and opacity > 0.5:
                kind = "CANOPY" if g > r and g > b else "other"
                print(f"  GID {gid:3d} (row {row}, col {col:2d}) RGB({r:3d},{g:3d},{b:3d}) op={opacity:.2f} {kind}")

# Outdoor tilesheet - find fence/structure tiles (rows 10-18)
print("\n=== OUTDOOR SHEET: Structure tiles (rows 10-18) ===")
for row in range(10, 18):
    for col in range(out_cols):
        info = tile_info(img, row, col)
        if info:
            r, g, b, opacity = info
            gid = row * out_cols + col + 1
            if opacity > 0.8 and not (g > 120 and g > r and g > b):  # non-green, opaque
                print(f"  GID {gid:3d} (row {row:2d}, col {col:2d}) RGB({r:3d},{g:3d},{b:3d}) op={opacity:.2f}")

# Town tilesheet - identify a simple house structure
# Look at rows 28-34, cols 0-10 area (small wooden cabin visible in image)
print("\n=== TOWN SHEET: Small cabin area (rows 28-34, cols 0-10) ===")
town_img = Image.open(os.path.join(ASSETS, "spring_town.png")).convert("RGBA")
town_cols = 32
for row in range(28, 35):
    tiles = []
    for col in range(11):
        info = tile_info(town_img, row, col, cols=town_cols)
        if info:
            r, g, b, opacity = info
            gid = 2503 + row * town_cols + col
            tiles.append(f"{gid}{'*' if opacity < 0.5 else ' '}")
        else:
            tiles.append("....  ")
    print(f"  Row {row}: {' '.join(tiles)}")

# Town tilesheet - look at rows 37-43 (fountain/plaza area)
print("\n=== TOWN SHEET: Fountain/plaza area (rows 37-43) ===")
for row in range(37, 44):
    tiles = []
    for col in range(town_cols):
        info = tile_info(town_img, row, col, cols=town_cols)
        if info:
            r, g, b, opacity = info
            sym = "." if opacity < 0.3 else "#" if opacity > 0.8 else "~"
        else:
            sym = " "
        tiles.append(sym)
    print(f"  Row {row}: {''.join(tiles)}")

# Also find well/fountain structures in the town sheet
print("\n=== TOWN SHEET: Searching for stone/fountain tiles ===")
for row in range(35, 45):
    for col in range(town_cols):
        info = tile_info(town_img, row, col, cols=town_cols)
        if info:
            r, g, b, opacity = info
            gid = 2503 + row * town_cols + col
            # Stone/gray with high opacity
            if opacity > 0.8 and abs(r-g) < 40 and abs(g-b) < 40 and r > 80 and r < 180:
                print(f"  GID {gid} (row {row}, col {col:2d}) RGB({r:3d},{g:3d},{b:3d}) stone/gray")
