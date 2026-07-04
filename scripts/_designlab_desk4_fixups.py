"""Two desk4 plate fixes:
1. cards-a-cut: the flood-fill cut ate the strip between the top-right card's
   top ink edge and its first ruled line (card touches the plate border, cream
   on cream). RGB survived under alpha==0, so repair = column scan, re-opaque
   the gap between the surviving ink fringe and the solid body.
2. book-d-cut: split into desk-level wash splash (paints UNDER the card pile)
   and the solid book (paints OVER it). The splash is opaque paint inside the
   silhouette, so split by reachability: flood from the borders across
   non-ink pixels; whatever the flood reaches without crossing the book's
   dark outline is wash.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

LW = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\design-lab\assets\lw"

# ---- 1. cards strip repair ----
p = LW + r"\desk4-cards-a-cut.png"
im = np.array(Image.open(p))
a = im[:, :, 3]
fixed_cols = 0
for x in range(1150, 2060):
    col = a[:320, x]
    nz = np.nonzero(col > 0)[0]
    if not len(nz):
        continue
    top_ink = nz[0]
    solid = np.nonzero(col == 255)[0]
    if not len(solid):
        continue
    body = solid[0]
    if 4 < body - top_ink < 350:
        a[top_ink + 1:body, x] = 255
        # make the surviving ink fringe row solid enough to read as the edge
        a[top_ink, x] = max(a[top_ink, x], 160)
        fixed_cols += 1
Image.fromarray(im).save(p)
print(f"cards: repaired {fixed_cols} columns")

# ---- 2. book wash/solid split ----
book = np.array(Image.open(LW + r"\desk4-book-d-cut.png"))
r, g, b, ba = [book[:, :, i].astype(np.int32) for i in range(4)]
lum = (299 * r + 587 * g + 114 * b) // 1000
barrier = (ba > 0) & (lum < 110)          # the book's dark ink outline
barrier = ndimage.binary_closing(barrier, np.ones((5, 5)))  # seal AA gaps
floodable = ~barrier
lbl, n = ndimage.label(floodable)
edge_labels = set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1])
edge_labels.discard(0)
outside = np.isin(lbl, list(edge_labels))
wash_m = outside & (ba > 0)
solid_m = (ba > 0) & ~wash_m
print(f"book: wash px {int(wash_m.sum())}, solid px {int(solid_m.sum())}")

# overlap the seam by 2px each way — same source pixels, so no visible join
wash_d = ndimage.binary_dilation(wash_m, iterations=2) & (ba > 0)
solid_d = ndimage.binary_dilation(solid_m, iterations=2) & (ba > 0)

for name, m in (("wash", wash_d), ("solid", solid_d)):
    out = book.copy()
    out[:, :, 3] = np.where(m, book[:, :, 3], 0)
    Image.fromarray(out).save(LW + rf"\desk4-book-d-{name}.png")
    print(f"wrote desk4-book-d-{name}.png")

# proof sheet: wash layer alone on a mid grey
h, w = ba.shape
proof = np.full((h, w, 3), 128, np.uint8)
wash_img = np.array(Image.open(LW + r"\desk4-book-d-wash.png")).astype(np.float32)
al = wash_img[:, :, 3:4] / 255.0
proof = (proof * (1 - al) + wash_img[:, :, :3] * al).astype(np.uint8)
Image.fromarray(proof).resize((900, int(900 * h / w))).save(
    r"C:\Users\tshau\Downloads\book-wash-proof.png")
print("proof written")
