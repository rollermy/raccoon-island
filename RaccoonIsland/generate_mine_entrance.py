"""Generate a 16x16 mine entrance (ladder hole) sprite for RaccoonIsland mod."""
from PIL import Image

img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
px = img.putpixel

STONE = (100, 90, 80, 255)
STONE_LT = (130, 120, 110, 255)
STONE_DK = (70, 60, 50, 255)
HOLE = (20, 15, 10, 255)
RUNG = (140, 110, 60, 255)
RUNG_DK = (110, 85, 40, 255)

# Stone border (outer ring)
for x in range(16):
    px((x, 0), STONE_LT)
    px((x, 15), STONE_DK)
for y in range(16):
    px((0, y), STONE_LT)
    px((15, y), STONE_DK)
# Corner highlights
px((0, 0), STONE_LT)
px((15, 0), STONE)
px((0, 15), STONE)
px((15, 15), STONE_DK)
# Inner stone border
for x in range(1, 15):
    px((x, 1), STONE)
    px((x, 14), STONE_DK)
for y in range(1, 15):
    px((1, y), STONE)
    px((14, y), STONE_DK)

# Dark hole interior
for y in range(2, 14):
    for x in range(2, 14):
        px((x, y), HOLE)

# Ladder rails (vertical, left and right inside the hole)
for y in range(2, 14):
    px((4, y), RUNG_DK)
    px((11, y), RUNG_DK)

# Ladder rungs (horizontal bars)
for rung_y in (4, 7, 10, 13):
    for x in range(4, 12):
        px((x, rung_y), RUNG)
    px((4, rung_y), RUNG_DK)
    px((11, rung_y), RUNG_DK)

img.save("assets/mine_entrance.png")
print("Created assets/mine_entrance.png (16x16)")
