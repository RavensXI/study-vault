"""Build desk4-scene-clean.png — the 'clean desk' state.

Start from the PRE-stain-surgery scene (git 4e8f8c19), heal the coffee ring
and ink splat at their original positions (no re-stamp), then lift the desk
clutter (yellow stub, eraser, fountain pen, shavings, pencil, crumbs) with
object-mask healing: saturated-or-inked pixels, dilated, hole-filled, then
dilated wide enough to swallow each object's soft shadow, blended with a
same-row grain patch. The mug, radio, and postcard photo stay — they are
equipment, not mess. Order matters: stains first, so clutter patches can
borrow from the ex-ring zone.
"""
import subprocess
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_dilation, binary_fill_holes

ROOT = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox"
OUT = ROOT + r"\design-lab\assets\lw\desk4-scene-clean.png"
BASE_COMMIT = "4e8f8c19"  # pre-surgery scene

raw = subprocess.run(["git", "-C", ROOT, "show",
                      f"{BASE_COMMIT}:design-lab/assets/lw/desk4-scene-a.png"],
                     capture_output=True).stdout
import io
im = np.array(Image.open(io.BytesIO(raw)).convert("RGB")).astype(np.float64)

def edge_feather(h, w, r=26):
    e = np.ones((h, w))
    ramp = np.linspace(0, 1, r)
    e[:r, :] *= ramp[:, None]; e[-r:, :] *= ramp[::-1][:, None]
    e[:, :r] *= ramp[None, :]; e[:, -r:] *= ramp[::-1][None, :]
    return e

def heal_stain(x0, y0, x1, y1, bg_dx, thresh):
    h, w = y1 - y0, x1 - x0
    src = im[y0:y1, x0:x1].copy()
    bg = im[y0:y1, x0 + bg_dx:x1 + bg_dx].copy()
    ratio = np.clip(src / np.maximum(bg, 1.0), 0.0, 1.25)
    stain = np.clip(1.0 - ratio.mean(axis=2), 0.0, 1.0)
    alpha = np.clip(gaussian_filter((stain > thresh).astype(np.float64), 6) * 1.6, 0, 1)
    alpha = (alpha * edge_feather(h, w))[..., None]
    im[y0:y1, x0:x1] = src * (1 - alpha) + bg * alpha
    print(f"stain healed ({x0},{y0})-({x1},{y1})")

def lift_object(x0, y0, x1, y1, bg_dx):
    """Wholesale feathered box replace — the bg patch is same-row grain, so
    over-replacing is harmless and no object sliver can survive a tight mask."""
    h, w = y1 - y0, x1 - x0
    src = im[y0:y1, x0:x1].copy()
    bg = im[y0:y1, x0 + bg_dx:x1 + bg_dx].copy()
    m = edge_feather(h, w, r=44)[..., None]
    im[y0:y1, x0:x1] = src * (1 - m) + bg * m
    print(f"lifted ({x0},{y0})-({x1},{y1})")

# stains at ORIGINAL positions (same boxes as _designlab_desk4_stains.py)
heal_stain(1600, 660, 1910, 950, -450, 0.05)   # coffee ring
heal_stain(90, 1140, 450, 1440, 510, 0.06)     # ink splat

# clutter (bg patches shift left into the now-clean centre desk, same rows)
lift_object(1850, 530, 2070, 760, -700)        # yellow pencil stub
lift_object(2050, 555, 2240, 730, -700)        # eraser
lift_object(1890, 650, 2150, 950, -700)        # fountain pen
lift_object(2090, 630, 2390, 910, -700)        # pencil shavings
lift_object(2200, 470, 2570, 850, -800)        # pencil
lift_object(2360, 890, 2480, 985, -800)        # crumbs
lift_object(1950, 540, 2130, 710, -840)        # stub cap (bg at -700 has a speck)
lift_object(2230, 450, 2430, 560, -800)        # specks above the pencil

# the SECOND ink splatter (left-centre, mostly under the book but its left
# droplets peek out) + stray marks Tom can still see. Donor columns picked
# to dodge the two wood knots (keep those - character, not mess).
lift_object(380, 700, 780, 1290, 920)          # second splatter cluster
lift_object(90, 1130, 470, 1450, 1200)         # faint specks the stain thresh missed
lift_object(60, 665, 150, 760, 500)            # coffee smudge below the radio
lift_object(410, 260, 490, 330, 300)           # specks above the book
lift_object(1120, 230, 1280, 330, 400)         # faint drips top-centre

Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save(OUT)
print("wrote", OUT)
