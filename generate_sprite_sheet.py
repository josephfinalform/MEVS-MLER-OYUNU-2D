"""Generate sprite sheet by extracting char.png body parts and animating them."""

from PIL import Image
import math
import os

SRC = Image.open(os.path.join(os.path.dirname(__file__), 'char.png')).convert('RGBA')
SW, SH = SRC.size
px = list(SRC.getdata())

def sget(x, y):
    if 0 <= x < SW and 0 <= y < SH:
        c = px[y * SW + x]
        if c[3] > 20:
            return c
    return None

# Extract body parts from char.png
body_surf = Image.new('RGBA', (SW, 57), (0,0,0,0))
left_leg = Image.new('RGBA', (SW//2, SH-57), (0,0,0,0))
right_leg = Image.new('RGBA', (SW//2, SH-57), (0,0,0,0))
lw = SW // 2  # 21

for y in range(57):
    for x in range(SW):
        c = sget(x, y)
        if c:
            body_surf.putpixel((x, y), c)

for y in range(57, SH):
    for x in range(SW):
        c = sget(x, y)
        if c:
            ly = y - 57
            if x < lw:
                left_leg.putpixel((x, ly), c)
            else:
                right_leg.putpixel((x - lw, ly), c)

FW, FH = 48, 76
CENTER_X = (FW - SW) // 2

def render_frame(body_y=0, left_off=0, right_off=0, left_y=0, right_y=0,
                 arm_wave=False, arm_point=False, arm_up=False):
    """Render a single frame by compositing body parts."""
    img = Image.new('RGBA', (FW, FH), (0,0,0,0))
    
    # Body
    img.paste(body_surf, (CENTER_X, body_y), body_surf)
    
    # Legs
    leg_y = body_y + 57
    img.paste(left_leg, (CENTER_X + left_off, leg_y + left_y), left_leg)
    img.paste(right_leg, (CENTER_X + lw + right_off, leg_y + right_y), right_leg)
    
    # Clear overlapping original leg area to prevent ghosting
    # The leg region in body is rows 57+, overwrite with shifted legs only
    # We already paste legs, but the original body includes legs at rows 57+.
    # We need to clear the original leg area after pasting body.
    # Re-paste body but only rows 0-56 (already done above)
    # Legs start at row 57. Since body_surf only has rows 0-56, there's no ghosting!
    # Wait - actually body_surf has rows 0-56 which doesn't include the legs.
    # But char.png rows 48-56 include the hip area which connects to legs.
    # The legs are rows 57-74. So body with rows 0-56 doesn't include legs. Good!
    
    # Hand gestures
    if arm_wave:
        hx = FW - 12
        hy = body_y + 18
        for dy in range(5):
            for dx in range(4):
                img.putpixel((hx+dx, hy+dy), (210,180,180,255))
        for f in range(3):
            img.putpixel((hx+1+f, hy-1), (200,170,170,255))
    if arm_point:
        hx = FW - 10
        hy = body_y + 38
        for dy in range(4):
            for dx in range(4):
                if hx+dx < FW:
                    img.putpixel((hx+dx, hy+dy), (210,180,180,255))
        for fx in range(4):
            if hx+4+fx < FW:
                img.putpixel((hx+4+fx, hy+1), (200,170,170,255))
    if arm_up:
        for side, x_off in [(-1, 6), (1, FW-10)]:
            hy = body_y + 14
            for dy in range(5):
                for dx in range(4):
                    if x_off+dx < FW:
                        img.putpixel((x_off+dx, hy+dy), (210,180,180,255))
    
    return img


frames = []
labels = []

# ── Walk cycle (6 frames) ──
for i in range(6):
    t = i * math.pi / 3
    left = int(round(5 * math.sin(t)))
    right = int(round(5 * math.sin(t + math.pi)))
    hop = abs(int(round(2 * math.sin(t + 0.5))))
    img = render_frame(body_y=2-hop, left_off=left, right_off=right,
                       left_y=-hop, right_y=-hop)
    frames.append(img); labels.append('W')

# ── Jump (4 frames) ──
poses = [
    (4, 0, 0, 4, 4, False, False, False),   # crouch
    (-6, 0, 0, 0, 0, False, False, False),   # rising
    (-10, 0, 0, -4, -4, False, False, False), # apex
    (5, 0, 0, 5, 5, False, False, False),     # landing
]
for by, lo, ro, ly, ry, aw, ap, au in poses:
    img = render_frame(body_y=by, left_off=lo, right_off=ro,
                       left_y=ly, right_y=ry, arm_wave=aw, arm_point=ap, arm_up=au)
    frames.append(img); labels.append('J')

# ── Gestures (3 frames) ──
# Wave
img = render_frame(body_y=0, left_off=0, right_off=0,
                   left_y=0, right_y=0, arm_wave=True)
frames.append(img); labels.append('G')

# Point
img = render_frame(body_y=0, left_off=0, right_off=0,
                   left_y=0, right_y=0, arm_point=True)
frames.append(img); labels.append('G')

# Both arms up
img = render_frame(body_y=-2, left_off=0, right_off=0,
                   left_y=0, right_y=0, arm_up=True)
frames.append(img); labels.append('G')


# ── Assemble sheet ──
cols = 6
rows = (len(frames) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * FW, rows * FH), (0,0,0,0))

for i, f in enumerate(frames):
    col = i % cols
    row = i // cols
    sheet.paste(f, (col * FW, row * FH), f)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprite_sheet.png')
sheet.save(out_path, 'PNG')
print(f"Saved: {out_path}")
print(f"Grid: {cols}x{rows}, Frame: {FW}x{FH}, Total: {len(frames)} frames")
for i, lbl in enumerate(labels):
    nz = sum(1 for p in list(frames[i].getdata()) if p[3] > 20)
    print(f"  {i}: {lbl} ({nz} px)")
