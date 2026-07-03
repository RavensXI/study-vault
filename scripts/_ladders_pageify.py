"""Lift the drawing off the plate: convert each subject-ladder image into an
'ink on transparent' PNG so it sits directly ON the notebook page — no box.
Alpha per pixel = how much darker than the plate's own paper tone it is:
paper -> fully transparent, thin washes -> translucent tint, ink -> opaque.
Writes {name}-page.png alongside each; safe to re-run (skips existing).
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAD = os.path.join(ROOT, "design-lab", "assets", "lw", "ladders")

count = 0
for f in sorted(os.listdir(LAD)):
    if not f.endswith(".png") or f.endswith("-page.png"):
        continue
    out = os.path.join(LAD, f.replace(".png", "-page.png"))
    if os.path.exists(out):
        continue
    im = Image.open(os.path.join(LAD, f)).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    # the plate's own paper tone: bright percentile per channel
    paper = np.percentile(a.reshape(-1, 3), 92, axis=0)
    # darkness relative to paper, strongest channel wins (keeps coloured washes)
    d = np.clip((paper - a) / np.maximum(paper, 1), 0, 1).max(axis=2)
    alpha = np.clip(d * 1.25, 0, 1)
    # edge feather: plates often darken toward their edges or draw themselves a
    # faint frame — ramp alpha to zero over the outer 9% so no border survives
    h, w = alpha.shape
    fy = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / (h * 0.09), 0, 1)
    fx = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / (w * 0.09), 0, 1)
    ramp = np.minimum.outer(fy, fx)
    alpha = alpha * (ramp * ramp * (3 - 2 * ramp))          # smoothstep
    alpha = (alpha * 255).astype(np.uint8)
    rgba = np.dstack([a.astype(np.uint8), alpha])
    Image.fromarray(rgba, "RGBA").save(out)
    count += 1
    print("ok  ", f, "->", os.path.basename(out))
print(f"done: {count} pageified")
