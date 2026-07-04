"""Relocate the coffee ring and ink splat in desk4-scene-a.png so they are not
buried under the (HTML) book and card pile.

Method: the stains are translucent marks multiplied over wood grain. For each,
take a clean same-row background patch (same horizontal grain lines), compute
ratio = src/bg (the stain as a multiplicative layer, grain cancelled), heal the
source area with the background patch, and stamp the ratio onto the destination
(dst *= ratio), all under a soft feathered mask so edges vanish.

Ring: (1600,660)-(1910,950)  ->  centred near (2030,560), below the pencil mug.
Splat: (90,1140)-(450,1440)  ->  centred near (2060,1170), by the pen nib.
"""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

P = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\design-lab\assets\lw\desk4-scene-a.png"
im = np.array(Image.open(P).convert("RGB")).astype(np.float64)

def move_stain(sx0, sy0, sx1, sy1, bg_dx, dcx, dcy, thresh=0.05):
    h, w = sy1 - sy0, sx1 - sx0
    src = im[sy0:sy1, sx0:sx1].copy()
    bg  = im[sy0:sy1, sx0 + bg_dx:sx1 + bg_dx].copy()
    ratio = np.clip(src / np.maximum(bg, 1.0), 0.0, 1.25)
    ratio_stamp = np.minimum(ratio, 1.0)  # never brighten the destination
    stain = np.clip(1.0 - ratio.mean(axis=2), 0.0, 1.0)
    core = (stain > thresh).astype(np.float64)
    alpha = np.clip(gaussian_filter(core, 6) * 1.6, 0.0, 1.0)
    # kill anything near the bbox border so seams can't happen
    edge = np.ones((h, w))
    r = 26
    ramp = np.linspace(0, 1, r)
    edge[:r, :] *= ramp[:, None]; edge[-r:, :] *= ramp[::-1][:, None]
    edge[:, :r] *= ramp[None, :]; edge[:, -r:] *= ramp[::-1][None, :]
    alpha = (alpha * edge)[..., None]
    # heal the source
    im[sy0:sy1, sx0:sx1] = src * (1 - alpha) + bg * alpha
    # stamp at destination: multiply the stain into whatever grain is there
    dx0, dy0 = dcx - w // 2, dcy - h // 2
    dst = im[dy0:dy0 + h, dx0:dx0 + w]
    im[dy0:dy0 + h, dx0:dx0 + w] = dst * (1 - alpha * (1 - ratio_stamp))
    print(f"moved ({sx0},{sy0})-({sx1},{sy1}) -> centre ({dcx},{dcy}), "
          f"stain px {int((alpha > .5).sum())}")

# coffee ring: bg patch 450px to the left (clear wood, same rows)
move_stain(1600, 660, 1910, 950, -450, 2030, 560, thresh=0.05)
# ink splat: bg patch 510px to the right of src (clear wood, same rows)
move_stain(90, 1140, 450, 1440, 510, 2060, 1170, thresh=0.06)

Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save(P)
print("scene saved")
