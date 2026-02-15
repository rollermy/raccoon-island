"""Generate a 48x80 (3x5 tiles) raccoon god statue sprite.

Top 48x48: raccoon figure with crown
Bottom 48x32: 3x2 stone pedestal base (3 tiles wide)
"""
from PIL import Image

img = Image.new("RGBA", (48, 80), (0, 0, 0, 0))
px = img.putpixel

# Colors
STONE = (140, 135, 130, 255)
STONE_LT = (170, 165, 160, 255)
STONE_DK = (100, 95, 90, 255)
STONE_VDK = (70, 65, 60, 255)
FUR = (80, 75, 70, 255)
FUR_LT = (110, 105, 95, 255)
FUR_DK = (55, 50, 45, 255)
MASK = (45, 40, 35, 255)       # dark raccoon mask
EYE = (200, 180, 50, 255)      # glowing golden eyes
CROWN = (200, 170, 40, 255)    # gold crown
CROWN_DK = (160, 130, 30, 255)
NOSE = (30, 25, 20, 255)

# --- Pedestal base (y=48-79, bottom 32 rows = 3x2 tiles, full 3-tile width) ---
for y in range(48, 80):
    for x in range(48):
        t = (y - 48) / 31.0  # 0 at top, 1 at bottom
        margin = int((1.0 - t) * 2)  # slight taper
        if margin <= x < 48 - margin:
            if y == 48:
                px((x, y), STONE_LT)
            elif y == 49:
                px((x, y), STONE_LT)
            elif y >= 78:
                px((x, y), STONE_VDK)
            elif x <= margin + 1 or x >= 47 - margin - 1:
                px((x, y), STONE_DK)
            else:
                if (x * 7 + y * 3) % 13 == 0:
                    px((x, y), STONE_LT)
                elif (x * 5 + y * 11) % 17 == 0:
                    px((x, y), STONE_DK)
                else:
                    px((x, y), STONE)

# Horizontal mortar line
for x in range(2, 46):
    t = (64 - 48) / 31.0
    margin = int((1.0 - t) * 2)
    if margin <= x < 48 - margin:
        px((x, 64), STONE_DK)

# Vertical mortar lines
for line_x in [16, 32]:
    for y in range(50, 64):
        px((line_x, y), STONE_DK)
for line_x in [10, 24, 38]:
    for y in range(66, 78):
        px((line_x, y), STONE_DK)

# --- Raccoon body (y=14-47, sits on top of pedestal) ---
body_cx = 24.0
for y in range(14, 48):
    t = (y - 14) / 34.0  # 0 at top, 1 at bottom
    if t < 0.1:
        half_w = 6 + t * 30   # neck
    elif t < 0.5:
        half_w = 9 + (t - 0.1) * 10  # chest/belly widening
    else:
        half_w = 13 + (t - 0.5) * 6  # lower body

    for x in range(48):
        dx = abs(x - body_cx)
        if dx <= half_w:
            if dx > half_w - 1.5:
                px((x, y), FUR_DK)
            elif dx > half_w - 3:
                px((x, y), FUR)
            else:
                if dx < 5 and t > 0.15 and t < 0.8:
                    px((x, y), FUR_LT)
                else:
                    px((x, y), FUR)

# Arms crossed over belly (y=28-38)
for y in range(28, 38):
    t = (y - 28) / 10.0
    arm_x = int(14 + t * 8)
    for dx in range(-2, 3):
        ax = arm_x + dx
        if 8 < ax < 40:
            px((ax, y), FUR_DK)
    arm_x = int(34 - t * 8)
    for dx in range(-2, 3):
        ax = arm_x + dx
        if 8 < ax < 40:
            px((ax, y), FUR_DK)

# Tail on the right (y=36-47)
for y in range(36, 48):
    t = (y - 36) / 12.0
    tail_x = int(34 + t * 5)
    for dx in range(-2, 3):
        tx = tail_x + dx
        if 0 <= tx < 48:
            if (y % 3) == 0:
                px((tx, y), FUR_DK)
            else:
                px((tx, y), FUR_LT)

# --- Head (y=4-14) ---
head_cx, head_cy = 24.0, 9.0
head_rx, head_ry = 10.0, 7.0

for y in range(2, 16):
    for x in range(10, 38):
        dx = (x - head_cx) / head_rx
        dy = (y - head_cy) / head_ry
        if dx * dx + dy * dy <= 1.0:
            px((x, y), FUR)

# Ears
for dy in range(5):
    for dx in range(-2, 3):
        ex, ey = 17 + dx, 2 + dy - 3
        if 0 <= ey < 80 and 0 <= ex < 48:
            px((ex, ey), FUR_DK if abs(dx) > 1 else FUR)
        ex, ey = 31 + dx, 2 + dy - 3
        if 0 <= ey < 80 and 0 <= ex < 48:
            px((ex, ey), FUR_DK if abs(dx) > 1 else FUR)

# Raccoon mask (dark band across eyes)
for y in range(7, 11):
    for x in range(15, 34):
        dx = (x - head_cx) / head_rx
        dy = (y - head_cy) / head_ry
        if dx * dx + dy * dy <= 0.85:
            px((x, y), MASK)

# Eyes (glowing gold)
for dy in range(-1, 2):
    for dx in range(-1, 2):
        px((20 + dx, 9 + dy), EYE)
        px((28 + dx, 9 + dy), EYE)
# Eye pupils
px((20, 9), CROWN_DK)
px((28, 9), CROWN_DK)

# Nose
px((24, 11), NOSE)
px((23, 11), NOSE)
px((25, 11), NOSE)
px((24, 12), FUR_LT)

# --- Crown (y=0-4) ---
crown_points = [16, 20, 24, 28, 32]
for cp in crown_points:
    for y in range(0, 3):
        px((cp, y), CROWN)
        if cp > 16:
            px((cp - 1, y + 1), CROWN_DK)
        if cp < 32:
            px((cp + 1, y + 1), CROWN_DK)

# Crown band
for x in range(15, 34):
    dx = (x - head_cx) / head_rx
    if abs(dx) < 0.95:
        px((x, 3), CROWN)
        px((x, 4), CROWN_DK)

img.save("assets/raccoon_god.png")
print("Created assets/raccoon_god.png (48x80, 3x5 tiles)")
