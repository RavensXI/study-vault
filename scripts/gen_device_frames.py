# -*- coding: utf-8 -*-
"""Paint the two device frames on the welcome page (a portrait phone, a landscape tablet)
in the shelf's line-and-wash hand, via gpt-image-2.5-sunburst with the shelf lamp as the
reference for the hand. The screen is painted as flat magenta so it can be keyed out to a
transparent hole; the real lesson page sits behind the hole. Exports
assets/lw/shelf/device_{phone,tablet}.webp and writes the screen rectangle (fractions of
the cropped image) to scripts/_device_frames.json for the CSS.
Run: python scripts/gen_device_frames.py [phone|tablet] [--quality high]"""
import io, os, sys, json, base64, time, requests
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, gaussian_filter, label as cclabel

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "lw", "shelf")
RAW = os.path.join(ROOT, "_frames_raw")
KEY = os.environ["OPENAI_API_KEY"]
META = os.path.join(HERE, "_device_frames.json")
PAPER = (246, 241, 231)

DEVICES = {
    "phone": ("1024x1536", "a modern smartphone seen square-on in PORTRAIT, filling most of the frame height: a slim body "
              "with gently rounded corners, a thin dark-bronze rim with a warm brass edge line, a small pill-shaped camera "
              "island at the top of the screen, tiny side keys"),
    "tablet": ("1536x1024", "a modern tablet seen square-on in LANDSCAPE, filling most of the frame width: a slim body with "
               "rounded corners, a thin dark-bronze rim with a warm brass edge line, a small round camera dot centred on "
               "the long bezel, even bezels all round"),
}

def ref_png():
    im = Image.open(os.path.join(OUT, "lamp.webp")).convert("RGBA")
    W, H = 1024, 1024
    scale = (H * 0.8) / im.height
    im = im.resize((max(1, round(im.width * scale)), round(im.height * scale)), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), PAPER + (255,))
    bg.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2))
    b = io.BytesIO(); bg.convert("RGB").save(b, "PNG"); return b.getvalue()

def prompt_for(desc):
    return ("The attached image is a finished painting of a brass reading lamp: clean pen-and-ink linework with thin "
            "watercolour washes, warm brass and bronze tones, on plain pale warm paper. Paint in EXACTLY this hand: "
            + desc + ". The SCREEN is a flat, solid, uniform pure magenta rectangle (#FF00FF) with rounded corners, "
            "painted as one flat fill with NOTHING on it - no reflections, no highlights, no icons, no text, no gradient. "
            "The device is the only object; no shadow under it, no table, no hands; plain pale warm paper background "
            "(#f6f1e7); nothing else in frame.")

def gen(kind, quality):
    size, desc = DEVICES[kind]
    files = [("image[]", ("lamp.png", ref_png(), "image/png"))]
    data = {"model": "gpt-image-2.5-sunburst", "prompt": prompt_for(desc), "quality": quality,
            "size": size, "n": "1", "output_format": "png"}
    for attempt in range(3):
        r = requests.post("https://api.openai.com/v1/images/edits", headers={"Authorization": "Bearer " + KEY},
                          files=files, data=data, timeout=600)
        if r.status_code == 200:
            j = r.json(); u = j.get("usage", {})
            return Image.open(io.BytesIO(base64.b64decode(j["data"][0]["b64_json"]))).convert("RGB"), u
        print("  retry", attempt, r.status_code, r.text[:200], flush=True); time.sleep(8)
    raise RuntimeError("gen failed " + kind)

def cut_and_key(im):
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
    obj = binary_erosion(obj, iterations=2)
    obj = binary_fill_holes(obj)
    alpha = gaussian_filter(obj.astype(np.float64), 1.1)
    # the screen: magenta-ish pixels (high R and B, low G) - the biggest such blob, filled
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = (r > 150) & (b > 150) & (g < 110) & (np.abs(r - b) < 90)
    mag = binary_fill_holes(binary_dilation(mag, iterations=2))
    lab, n = cclabel(mag)
    if n > 1:
        sz = np.bincount(lab.ravel()); sz[0] = 0
        mag = lab == sz.argmax()
    ys, xs = np.where(mag)
    sy0, sy1, sx0, sx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    # the hole is the painted screen itself (rounded corners, camera island left in), grown a
    # pixel to eat the magenta fringe; the page sits square behind the hole's bounding box
    hole = binary_dilation(mag, iterations=1)
    alpha[hole] = 0.0
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
    W, H = x1 - x0, y1 - y0
    rect = {"left": (sx0 - x0) / W, "top": (sy0 - y0) / H, "width": (sx1 - sx0) / W, "height": (sy1 - sy0) / H,
            "px": [int(W), int(H)], "screen_px": [int(sx1 - sx0), int(sy1 - sy0)]}
    return Image.fromarray(rgba, "RGBA"), rect

if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    quality = "high" if "--quality" in sys.argv and "high" in sys.argv else "medium"
    meta = json.load(open(META)) if os.path.exists(META) else {}
    os.makedirs(RAW, exist_ok=True)
    for kind in (args or list(DEVICES)):
        t0 = time.time()
        if "--reprocess" in sys.argv:           # re-cut the saved painting, no API call
            im, usage = Image.open(os.path.join(RAW, f"{kind}.png")).convert("RGB"), {}
        else:
            im, usage = gen(kind, quality)
            im.save(os.path.join(RAW, f"{kind}.png"))
        rgba, rect = cut_and_key(im)
        w = 1100 if kind == "tablet" else 640
        h = max(1, round(rgba.height * w / rgba.width))
        rgba.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, f"device_{kind}.webp"), quality=88, method=6)
        ot = usage.get("output_tokens", 0)
        cost = (usage.get("input_tokens_details", {}).get("text_tokens", 0) * 5 + usage.get("input_tokens_details", {}).get("image_tokens", 0) * 8 + ot * 30) / 1e6
        rect.update(usd=round(cost, 4), secs=round(time.time() - t0))
        meta[kind] = rect
        json.dump(meta, open(META, "w"), indent=1)
        print(kind, json.dumps(rect), flush=True)
