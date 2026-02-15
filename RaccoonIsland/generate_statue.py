"""Generate a 16x32 raccoon statue sprite for the RaccoonIsland mod."""
from PIL import Image

img = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
px = img.putpixel

STONE = (140, 140, 150, 255)
STONE_LT = (165, 165, 175, 255)
STONE_DK = (110, 110, 120, 255)
MASK = (60, 60, 65, 255)
EYE = (80, 200, 120, 255)  # green gem eyes
NOSE = (50, 50, 55, 255)
PED = (120, 115, 110, 255)
PED_LT = (145, 140, 135, 255)
PED_DK = (95, 90, 85, 255)
TAIL_DK = (60, 60, 65, 255)

# --- Pedestal (rows 26-31) ---
for y in range(28, 32):
    for x in range(1, 15):
        px((x, y), PED)
for y in range(28, 32):
    px((1, y), PED_LT)
    px((14, y), PED_DK)
for x in range(1, 15):
    px((x, 28), PED_LT)
    px((x, 31), PED_DK)
# pedestal top rim
for x in range(0, 16):
    px((x, 26), PED_LT)
    px((x, 27), PED)

# --- Body (rows 10-25) ---
for y in range(12, 26):
    for x in range(4, 12):
        px((x, y), STONE)
# shoulders wider
for y in range(12, 15):
    for x in range(3, 13):
        px((x, y), STONE)
# light edge left
for y in range(12, 26):
    if 4 <= 4:
        px((4, y), STONE_LT)
# dark edge right
for y in range(12, 26):
    px((11, y), STONE_DK)

# belly highlight
for y in range(16, 23):
    for x in range(6, 10):
        px((x, y), STONE_LT)

# --- Head (rows 2-11) ---
for y in range(4, 12):
    for x in range(3, 13):
        px((x, y), STONE)
# round top of head
for x in range(5, 11):
    px((x, 3), STONE)
for x in range(6, 10):
    px((x, 2), STONE)

# Ears
px((3, 3), STONE)
px((4, 2), STONE)
px((3, 2), STONE_LT)
px((12, 3), STONE)
px((11, 2), STONE)
px((12, 2), STONE_DK)

# --- Face mask (dark raccoon markings) ---
for x in range(4, 7):
    px((x, 6), MASK)
    px((x, 7), MASK)
for x in range(9, 12):
    px((x, 6), MASK)
    px((x, 7), MASK)

# Eyes (gem green)
px((5, 7), EYE)
px((10, 7), EYE)

# Nose
px((7, 9), NOSE)
px((8, 9), NOSE)

# Mouth line
px((7, 10), STONE_DK)
px((8, 10), STONE_DK)

# --- Tail (right side, rows 18-27) ---
px((12, 18), STONE)
px((13, 19), STONE)
px((13, 20), TAIL_DK)
px((14, 21), STONE)
px((14, 22), TAIL_DK)
px((13, 23), STONE)
px((13, 24), TAIL_DK)
px((12, 25), STONE)
px((12, 26), TAIL_DK)

# --- Arms/paws ---
for y in range(15, 19):
    px((3, y), STONE)
    px((12, y), STONE)
px((3, 19), STONE_DK)
px((12, 19), STONE_DK)

# --- Feet ---
px((5, 26), STONE)
px((6, 26), STONE)
px((9, 26), STONE)
px((10, 26), STONE)
px((5, 27), STONE_DK)
px((6, 27), STONE_DK)
px((9, 27), STONE_DK)
px((10, 27), STONE_DK)

img.save("assets/raccoon_statue.png")
print("Created assets/raccoon_statue.png (16x32)")
