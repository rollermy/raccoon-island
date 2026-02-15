"""Generate a 48x32 (3x2 tiles) raccoon nest sprite for tent interiors."""
from PIL import Image

img = Image.new("RGBA", (48, 32), (0, 0, 0, 0))
px = img.putpixel

TWIG = (139, 90, 43, 255)
TWIG_DK = (101, 67, 33, 255)
TWIG_LT = (180, 130, 70, 255)
STRAW = (190, 165, 110, 255)
STRAW_DK = (160, 140, 90, 255)
LEAF = (70, 110, 45, 255)
LEAF_DK = (50, 80, 30, 255)
BLANKET = (120, 70, 90, 255)  # muted plum

# Draw oval nest shape across the 48x32 canvas
cx, cy = 24.0, 16.0
rx, ry = 22.0, 14.0  # outer radii
rx_in, ry_in = 16.0, 9.0  # inner radii (cushion area)

# Small blanket ellipse offset to one side of the cushion
bx, by = 28.0, 14.0  # blanket center (right of center)
brx, bry = 8.0, 5.0  # blanket radii (small patch)

for y in range(32):
    for x in range(48):
        dx = (x - cx) / rx
        dy = (y - cy) / ry
        dist_outer = dx * dx + dy * dy

        dx_in = (x - cx) / rx_in
        dy_in = (y - cy) / ry_in
        dist_inner = dx_in * dx_in + dy_in * dy_in

        if dist_outer > 1.0:
            continue

        if dist_inner <= 1.0:
            # Check if this pixel is under the blanket
            bdx = (x - bx) / brx
            bdy = (y - by) / bry
            dist_blanket = bdx * bdx + bdy * bdy

            if dist_blanket <= 1.0:
                px((x, y), BLANKET)
            else:
                # Inner cushion — straw/hay fill
                if (x + y) % 5 == 0:
                    px((x, y), STRAW_DK)
                elif (x * 3 + y * 7) % 11 == 0:
                    px((x, y), TWIG_LT)
                else:
                    px((x, y), STRAW)
        else:
            # Twig rim
            if (x + y) % 3 == 0:
                px((x, y), TWIG_DK)
            elif (x * 7 + y) % 9 == 0:
                px((x, y), TWIG_LT)
            elif (x * 3 + y * 5) % 17 == 0:
                px((x, y), LEAF)
            elif (x + y * 3) % 19 == 0:
                px((x, y), LEAF_DK)
            else:
                px((x, y), TWIG)

# Add a few twig lines across the rim for texture
for x in range(4, 44):
    y_top = int(cy - ry * (1.0 - ((x - cx) / rx) ** 2) ** 0.5) if abs((x - cx) / rx) < 1 else None
    if y_top is not None and 0 <= y_top < 32:
        px((x, y_top + 1), TWIG_DK)
    y_bot = int(cy + ry * (1.0 - ((x - cx) / rx) ** 2) ** 0.5) if abs((x - cx) / rx) < 1 else None
    if y_bot is not None and 0 <= y_bot < 32:
        px((x, y_bot - 1), TWIG_DK)

img.save("assets/nest_tiles.png")
print("Created assets/nest_tiles.png (48x32, 3x2 tiles)")
