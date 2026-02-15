"""Generate a 48x48 tent tilesheet (3x3 grid of 16x16 tiles) for RaccoonIsland mod.

Matches the Stardew Valley tent style: golden A-frame canvas tent with
bright yellow highlights on the right, amber shadows on the left, center
ridge seam, and dark maroon door opening.

Layout:
  Row 0: [roof-left] [roof-peak] [roof-right]   -> Front layer (above player)
  Row 1: [wall-left] [wall-front] [wall-right]   -> Buildings layer (blocks movement)
  Row 2: [base-left] [door]       [base-right]   -> Buildings layer (door is gap)
"""
from PIL import Image

img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
px = img.putpixel

# Color palette — sampled from the vanilla Stardew Valley tent sprite
BRIGHT = (255, 241, 30, 255)     # bright yellow highlight (right/lit side)
MEDIUM = (255, 187, 5, 255)      # medium yellow (transition)
AMBER = (225, 153, 1, 255)       # golden amber (left/shadow side)
DARK_AMBER = (208, 126, 0, 255)  # deeper shadow
BROWN = (163, 95, 0, 255)        # darkest canvas edge
DOOR = (56, 17, 10, 255)         # dark maroon door opening
GROUND = (87, 55, 13, 191)       # semi-transparent pebbly ground
SEAM = (176, 107, 22, 255)       # center ridge seam
POLE = (102, 60, 22, 255)        # wooden pole


def canvas_color(x, tile_w=16):
    """Pick canvas color based on horizontal position (left=shadow, right=lit)."""
    t = x / max(tile_w - 1, 1)
    if t < 0.2:
        return BROWN
    elif t < 0.4:
        return DARK_AMBER
    elif t < 0.55:
        return AMBER
    elif t < 0.75:
        return MEDIUM
    else:
        return BRIGHT


# === Row 0: Roof (Front layer) — A-frame triangle, point at top-center ===

# Tile (0,0): roof-left — diagonal slope from top-right down to bottom-left
for y in range(16):
    # At y=0, canvas starts at x=15; at y=15, starts at x=0
    start_x = 15 - y
    for x in range(start_x, 16):
        # Map local x within the visible span to shadow->lit gradient
        span = 16 - start_x
        local_t = (x - start_x) / max(span - 1, 1)
        if local_t < 0.3:
            color = BROWN
        elif local_t < 0.6:
            color = DARK_AMBER
        else:
            color = AMBER
        px((x, y), color)
    # Leading edge highlight
    if start_x < 16:
        px((start_x, y), DARK_AMBER)

# Tile (1,0): roof-peak — full canvas, center seam, left=shadow right=lit
for y in range(16):
    for x in range(16):
        px((16 + x, y), canvas_color(x))
    # Center ridge seam
    px((16 + 7, y), SEAM)
    px((16 + 8, y), SEAM)

# Tile (2,0): roof-right — diagonal slope from top-left down to bottom-right
for y in range(16):
    end_x = y  # at y=0, canvas ends at x=0; at y=15, ends at x=15
    for x in range(0, end_x + 1):
        local_t = x / max(end_x, 1)
        if local_t < 0.4:
            color = MEDIUM
        elif local_t < 0.7:
            color = BRIGHT
        else:
            color = BRIGHT
        px((32 + x, y), color)
    # Trailing edge
    if end_x > 0:
        px((32 + end_x, y), MEDIUM)


# === Row 1: Walls (Buildings layer) — full canvas panels ===

# Tile (0,1): wall-left — shadow side
for y in range(16):
    for x in range(16):
        # Gradient: dark at left edge, amber toward center
        t = x / 15
        if t < 0.15:
            color = BROWN
        elif t < 0.35:
            color = DARK_AMBER
        elif t < 0.65:
            color = AMBER
        else:
            color = AMBER
        px((x, 16 + y), color)
    # Subtle vertical wrinkle lines
    if y % 4 == 0:
        px((4, 16 + y), DARK_AMBER)
        px((10, 16 + y), DARK_AMBER)

# Tile (1,1): wall-front — center, seam divides shadow/lit
for y in range(16):
    for x in range(16):
        px((16 + x, 16 + y), canvas_color(x))
    # Center ridge seam
    px((16 + 7, 16 + y), SEAM)
    px((16 + 8, 16 + y), SEAM)
    # Subtle fabric texture
    if y % 5 == 0:
        px((16 + 3, 16 + y), DARK_AMBER)
        px((16 + 12, 16 + y), MEDIUM)

# Tile (2,1): wall-right — lit side
for y in range(16):
    for x in range(16):
        t = x / 15
        if t < 0.35:
            color = MEDIUM
        elif t < 0.65:
            color = BRIGHT
        else:
            color = BRIGHT
        px((32 + x, 16 + y), color)
    # Subtle vertical wrinkle lines
    if y % 4 == 0:
        px((32 + 5, 16 + y), MEDIUM)
        px((32 + 11, 16 + y), MEDIUM)


# === Row 2: Base (Buildings layer, center is passable door) ===

# Tile (0,2): base-left — canvas narrows toward ground, shadow side
for y in range(16):
    for x in range(16):
        t = x / 15
        if t < 0.15:
            color = BROWN
        elif t < 0.35:
            color = DARK_AMBER
        else:
            color = AMBER
        px((x, 32 + y), color)
    # Ground at bottom rows
    if y >= 13:
        for x in range(16):
            px((x, 32 + y), GROUND)

# Tile (1,2): door — dark maroon opening with canvas arch at top
for y in range(16):
    for x in range(16):
        px((16 + x, 32 + y), DOOR)
    # Canvas arch over door top (triangular drape)
    if y <= 3:
        arch_inset = y * 2  # widens as we go down
        for x in range(arch_inset):
            px((16 + x, 32 + y), canvas_color(x))
        for x in range(16 - arch_inset, 16):
            px((16 + x, 32 + y), canvas_color(x))
    # Pole frame on sides
    px((16 + 0, 32 + y), POLE)
    px((16 + 15, 32 + y), POLE)
    # Ground at bottom
    if y >= 13:
        for x in range(16):
            px((16 + x, 32 + y), GROUND)

# Tile (2,2): base-right — canvas narrows toward ground, lit side
for y in range(16):
    for x in range(16):
        t = x / 15
        if t < 0.35:
            color = MEDIUM
        else:
            color = BRIGHT
        px((32 + x, 32 + y), color)
    # Ground at bottom rows
    if y >= 13:
        for x in range(16):
            px((32 + x, 32 + y), GROUND)

img.save("assets/tent_tiles.png")
print("Created assets/tent_tiles.png (48x48)")
