"""Re-cut the desk clutter plates with SOLID silhouettes.
The old alpha-from-darkness matte made pale bodies translucent (mug) and the
eraser plate was never cut at all. This does it properly:
  crop 5% (kills drawn frames) -> flood paper from the borders (connected
  components of paper-like tone) -> object = everything else, fully opaque ->
  distance-based softening ONLY in the outer boundary band so wash shadows
  still fade out -> despeckle -> trim to bbox -> overwrite {name}-cut.png.
Prints each cut's solid-fill fraction so CSS widths can be recalibrated
(visible px = css width x fill).
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LW = os.path.join(ROOT, "design-lab", "assets", "lw")

PLATES = ["night-pencil", "night-fountain-pen", "night-highlighter",
          "night-eraser", "night-pen-mug"]
THR = 30.0        # paper-likeness tolerance (euclidean RGB)
BAND = 6          # px of boundary band that may fade (wash shadows)

for name in PLATES:
    src = os.path.join(LW, name + ".png")
    im = Image.open(src).convert("RGB")
    w, h = im.size
    cx, cy = int(w * .05), int(h * .05)
    im = im.crop((cx, cy, w - cx, h - cy))
    a = np.asarray(im).astype(np.float32)
    H, W = a.shape[:2]

    ring = np.concatenate([a[:12].reshape(-1, 3), a[-12:].reshape(-1, 3),
                           a[:, :12].reshape(-1, 3), a[:, -12:].reshape(-1, 3)])
    paper = np.median(ring, axis=0)
    dist = np.sqrt(((a - paper) ** 2).sum(axis=2))
    paper_like = dist < THR

    # background = paper-like regions connected to the border
    lab, n = ndimage.label(paper_like)
    border_labels = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border_labels[border_labels != 0])
    mask = ~bg

    # despeckle: drop tiny floating specks of "object"
    lab2, n2 = ndimage.label(mask)
    sizes = ndimage.sum(mask, lab2, range(1, n2 + 1))
    keep = np.zeros(n2 + 1, bool); keep[1:] = sizes >= 120
    mask = keep[lab2]

    # solid interior; distance-fade only in the outer band (soft shadow edges)
    interior = ndimage.binary_erosion(mask, iterations=BAND)
    soft = np.clip(dist / THR, 0, 1)
    alpha = np.where(interior, 1.0, np.where(mask, soft * (3 - 2 * soft), 0.0))
    alpha = ndimage.gaussian_filter(alpha, 1.0) * mask   # AA without halo spread
    alpha8 = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)

    ys, xs = np.where(alpha8 > 8)
    pad = 6
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, H)
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, W)
    rgba = np.dstack([a.astype(np.uint8), alpha8])[y0:y1, x0:x1]
    out = os.path.join(LW, name + "-cut.png")
    Image.fromarray(rgba, "RGBA").save(out)

    solid = rgba[:, :, 3] > 128
    xs2 = np.where(solid.any(axis=0))[0]
    fill = (xs2.max() - xs2.min() + 1) / rgba.shape[1]
    print(f"{name}:  {rgba.shape[1]}x{rgba.shape[0]}  fill(w)={fill:.2f}")
print("done")
