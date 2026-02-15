#!/usr/bin/env python3
"""Find the best plain sand fill tiles from the beach tilesheet."""
from PIL import Image
import os

ASSETS = "/Users/jd/code/stardewvalley/extracted_assets"

def analyze_tile_uniformity(img, row, col, tile_size=16, cols=17):
    """Check how uniform a tile's color is (lower = more uniform = better fill tile)."""
    x0, y0 = col * tile_size, row * tile_size
    tile = img.crop((x0, y0, x0 + tile_size, y0 + tile_size))
    pixels = list(tile.getdata())

    opaque = [(r, g, b) for r, g, b, a in pixels if a > 128]
    if len(opaque) < 200:  # mostly transparent
        return None

    avg_r = sum(r for r, g, b in opaque) // len(opaque)
    avg_g = sum(g for r, g, b in opaque) // len(opaque)
    avg_b = sum(b for r, g, b in opaque) // len(opaque)

    # Calculate color variance (lower = more uniform)
    variance = sum(
        (r - avg_r)**2 + (g - avg_g)**2 + (b - avg_b)**2
        for r, g, b in opaque
    ) / len(opaque)

    return {
        'avg': (avg_r, avg_g, avg_b),
        'variance': variance,
        'opacity': len(opaque) / len(pixels),
        'is_sandy': avg_r > 150 and avg_g > 100 and avg_b < 120 and avg_r > avg_b * 1.3,
    }


# Beach tilesheet: 272x496 = 17 cols x 31 rows
img = Image.open(os.path.join(ASSETS, "spring_beach.png")).convert("RGBA")
cols = 17
rows = img.height // 16

print("Beach tilesheet: All tiles with sandy color, sorted by uniformity")
print("(Lower variance = more uniform = better for fill)")
print()

sandy_tiles = []
for row in range(rows):
    for col_idx in range(cols):
        info = analyze_tile_uniformity(img, row, col_idx, cols=cols)
        if info and info['is_sandy']:
            tile_id = row * 17 + col_idx
            sandy_tiles.append((tile_id, row, col_idx, info))

sandy_tiles.sort(key=lambda x: x[3]['variance'])

print(f"Found {len(sandy_tiles)} sandy tiles:")
for tile_id, row, col, info in sandy_tiles[:25]:
    tmx_gid = 1976 + tile_id  # with beach firstgid=1976
    print(f"  tile_id={tile_id:3d} (row {row:2d}, col {col:2d}) "
          f"GID={tmx_gid} RGB{info['avg']} "
          f"var={info['variance']:.0f} opacity={info['opacity']:.2f}")


# Also check outdoor tilesheet for the best water tiles
print("\n\nOutdoor tilesheet: Water tiles sorted by uniformity (dark blue)")
img2 = Image.open(os.path.join(ASSETS, "spring_outdoorsTileSheet.png")).convert("RGBA")
out_cols = 25

water_tiles = []
for row in range(img2.height // 16):
    for col_idx in range(out_cols):
        x0, y0 = col_idx * 16, row * 16
        tile = img2.crop((x0, y0, x0 + 16, y0 + 16))
        pixels = list(tile.getdata())
        opaque = [(r, g, b) for r, g, b, a in pixels if a > 128]
        if len(opaque) < 250:  # need mostly opaque
            continue
        avg_r = sum(r for r, g, b in opaque) // len(opaque)
        avg_g = sum(g for r, g, b in opaque) // len(opaque)
        avg_b = sum(b for r, g, b in opaque) // len(opaque)

        # Dark blue water
        if avg_b > 120 and avg_b > avg_r * 2 and avg_b > avg_g * 1.1:
            variance = sum(
                (r - avg_r)**2 + (g - avg_g)**2 + (b - avg_b)**2
                for r, g, b in opaque
            ) / len(opaque)
            tile_id = row * out_cols + col_idx
            gid = tile_id + 1
            water_tiles.append((gid, row, col_idx, avg_r, avg_g, avg_b, variance))

water_tiles.sort(key=lambda x: x[6])  # sort by variance
for gid, row, col, r, g, b, var in water_tiles[:15]:
    print(f"  GID={gid:4d} (row {row:2d}, col {col:2d}) RGB({r},{g},{b}) var={var:.0f}")
