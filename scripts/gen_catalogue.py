# -*- coding: utf-8 -*-
"""Paint the FAQ card catalogue on the welcome page in the shelf's line-and-wash hand (same
recipe as gen_device_frames.py: gpt-image-2.5-sunburst with the lamp as the style reference).
The six drawer label plates are painted flat magenta so they can be found; they are then
filled with plain card colour in the image and their rectangles (fractions of the cropped
image, ordered row by row) go to scripts/_device_frames.json under "catalogue" so the page
can overlay the six real-text labels. Exports assets/lw/shelf/catalogue.webp.
Run: python scripts/gen_catalogue.py [--reprocess] [--quality high]"""
import os, sys, json, time
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, gaussian_filter, label as cclabel
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_device_frames as G

DESC = ("a wooden library card-catalogue cabinet seen square-on, filling most of the frame width: a low "
        "rectangular oak cabinet with SIX drawer fronts in a grid of three across and two down, every drawer "
        "the same size, each drawer front with one small round brass pull handle at its centre and, just above "
        "the handle, a small flat rectangular label plate. EVERY label plate is a flat, solid, uniform pure "
        "magenta rectangle (#FF00FF), painted as one flat fill with NOTHING on it - no text, no highlight, no "
        "frame. Warm oak and walnut wood, thin dark-bronze linework, a slim plinth at the base")

def cut(im):
    a = np.array(im).astype(np.float64)
    corners = np.concatenate([a[:14, :14].reshape(-1, 3), a[:14, -14:].reshape(-1, 3),
                              a[-14:, :14].reshape(-1, 3), a[-14:, -14:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    obj = np.sqrt(((a - bg) ** 2).sum(axis=2)) > 30
    obj = binary_fill_holes(binary_dilation(obj, iterations=2))
    lab, n = cclabel(obj)
    if n > 1:
        sz = np.bincount(lab.ravel()); sz[0] = 0
        obj = lab == sz.argmax()
    obj = binary_fill_holes(binary_erosion(obj, iterations=2))
    alpha = gaussian_filter(obj.astype(np.float64), 1.1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = (r > 150) & (b > 150) & (g < 110) & (np.abs(r - b) < 90)
    mag = binary_fill_holes(binary_dilation(mag, iterations=2))
    lab, n = cclabel(mag)
    sz = np.bincount(lab.ravel()); sz[0] = 0
    keep = [i for i in range(1, n + 1) if sz[i] > 400]
    plates = []
    for i in keep:
        ys, xs = np.where(lab == i)
        plates.append((ys.min(), ys.max() + 1, xs.min(), xs.max() + 1))
    # fill every plate with plain card colour (a touch of the surrounding wash keeps it painted)
    fill = binary_dilation(np.isin(lab, keep), iterations=2)
    a[fill] = np.array([246, 239, 220])
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
    W, H = x1 - x0, y1 - y0
    # order the plates row by row, left to right
    plates.sort(key=lambda p: (round((p[0] - y0) / H, 1), p[2]))
    rects = [{"left": (px0 - x0) / W, "top": (py0 - y0) / H, "width": (px1 - px0) / W, "height": (py1 - py0) / H}
             for (py0, py1, px0, px1) in plates]
    return Image.fromarray(rgba, "RGBA"), {"px": [int(W), int(H)], "plates": rects}

if __name__ == "__main__":
    quality = "high" if "--quality" in sys.argv and "high" in sys.argv else "medium"
    meta = json.load(open(G.META)) if os.path.exists(G.META) else {}
    os.makedirs(G.RAW, exist_ok=True)
    raw = os.path.join(G.RAW, "catalogue.png")
    t0 = time.time()
    if "--reprocess" in sys.argv:
        im, usage = Image.open(raw).convert("RGB"), {}
    else:
        G.DEVICES["catalogue"] = ("1536x1024", DESC)
        im, usage = G.gen("catalogue", quality)
        im.save(raw)
    rgba, rect = cut(im)
    w = 1100; h = max(1, round(rgba.height * w / rgba.width))
    rgba.resize((w, h), Image.LANCZOS).save(os.path.join(G.OUT, "catalogue.webp"), quality=88, method=6)
    ot = usage.get("output_tokens", 0)
    cost = (usage.get("input_tokens_details", {}).get("text_tokens", 0) * 5 + usage.get("input_tokens_details", {}).get("image_tokens", 0) * 8 + ot * 30) / 1e6
    rect.update(usd=round(cost, 4), secs=round(time.time() - t0))
    meta["catalogue"] = rect
    json.dump(meta, open(G.META, "w"), indent=1)
    print(json.dumps(rect), flush=True)
