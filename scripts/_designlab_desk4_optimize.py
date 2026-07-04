"""Desk4 asset optimisation: PNG plates -> WebP, with the heavily-oversampled
object plates halved (they display at 0.2-0.5x even on 4K; layout is unaffected
because every <img class="plate"> has an explicit CSS width, so the browser
scales the smaller file into the same box). Scene + book plates keep full
resolution (they display largest).
Re-run after regenerating any plate.
"""
import os
from PIL import Image

LW = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\design-lab\assets\lw"

# (file, scale, quality)
PLATES = [
    ("desk4-scene-a.png",       1.0, 85),
    ("desk4-scene-clean.png",   1.0, 85),
    ("desk4-book-d-solid.png",  1.0, 88),
    ("desk4-book-d-wash.png",   1.0, 88),
    ("desk4-radio-a-cut.png",   0.5, 88),
    ("desk4-cards-a-cut.png",   0.5, 88),
    ("desk4-calendar-b-cut.png",0.5, 88),
    ("desk4-watch-a-cut.png",   0.5, 88),
    ("desk4-phone-c-cut.png",   0.5, 88),
]

tot_in = tot_out = 0
for name, scale, q in PLATES:
    src = os.path.join(LW, name)
    dst = os.path.join(LW, name[:-4] + ".webp")
    im = Image.open(src)
    if scale != 1.0:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=q, alpha_quality=90, method=6)
    si, so = os.path.getsize(src), os.path.getsize(dst)
    tot_in += si; tot_out += so
    print(f"{name:28s} {im.size[0]}x{im.size[1]}  {si//1024:5d} KB -> {so//1024:4d} KB")
print(f"\ntotal {tot_in/1e6:.1f} MB -> {tot_out/1e6:.1f} MB")
