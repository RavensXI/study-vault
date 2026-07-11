"""Atmosphere kit for the landing bookcase wall (Tom's art-direction notes 11 Jul):
  1. ledge with a VISIBLE TOP SURFACE (slight look-down) so objects can stand on it
  2. tone-on-tone wallpaper panel (two candidates: damask + stripe)
  3. shelf clutter in the line-and-wash style: plants, clock, hourglass, inkwell,
     horizontal book stack, globe — things end-of-run books can lean against.

Same pipeline as _designlab_shelf_books_all.py: gemini img2img, alpha-cut,
defringe, png+webp. Objects are prompted square-on, no cast shadow, plain pale
background so the cut is clean.

Run:            python scripts/_designlab_shelf_atmosphere.py [keys...]
Re-run safety:  skips existing outputs unless keys given.
"""
import io, os, sys, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, gaussian_filter, label as cclabel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

def on_white(path):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, (252, 249, 243, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB")

LAMP = on_white(os.path.join(OUT, "lamp.webp"))          # style reference (finished object)
LEDGE = Image.open(os.path.join(OUT, "ledge_walnut.webp")).convert("RGB")

STYLE = ("English line-and-wash watercolour illustration in EXACTLY the style of the attached "
         "brass lamp: confident warm sepia ink outlines, controlled transparent watercolour "
         "washes, believable material colour, plain pale warm paper background and NOTHING else "
         "in frame. The object is drawn STRAIGHT-ON at eye level (no three-quarter perspective, "
         "no visible top surface) and casts NO shadow. Exactly ONE object, filling most of the frame. ")

# key -> (prompt body, aspect)
OBJECTS = {
    "pot_ivy":   ("A small weathered terracotta plant pot with trailing ivy: a few long strands "
                  "of soft green leaves spilling over the rim and hanging down one side. The pot "
                  "is slightly wider than it is tall.", "3:4"),
    "pot_fern":  ("A compact potted fern in a cream glazed ceramic pot with a thin sage-green "
                  "band near the rim; short arching fronds, tidy and small.", "3:4"),
    "clock":     ("A small antique mantel clock: dark walnut case with a rounded top, round "
                  "brass-rimmed white dial with roman numerals, small brass feet.", "3:4"),
    "hourglass": ("A brass hourglass with three slim support columns, pale sand mostly in the "
                  "lower bulb.", "3:4"),
    "inkwell":   ("A small squat glass ink bottle with dark blue-black ink visible inside and a "
                  "brass cap, with a single white goose-feather quill standing in it, leaning "
                  "slightly to one side.", "3:4"),
    "bookstack": ("A short stack of two cloth hardback books lying flat, spines facing the "
                  "viewer: the lower book muted olive cloth, the upper deep oxblood cloth, both "
                  "with plain gold gilt band decorations on the spine (no words, no lettering). "
                  "The stack is wider than it is tall.", "4:3"),
    "globe":     ("A small desk globe on a brass stand and dark wooden base: aged sepia map "
                  "tones, slim brass meridian ring.", "3:4"),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(contents, aspect):
    for attempt in range(5):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=contents,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=aspect)))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

def cut(im):
    """bookend2-style alpha cut with pale-fringe removal (the halo fix)."""
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
    mn = a.min(axis=2)
    fringe = (alpha > 0.05) & (alpha < 0.95) & (mn > 212)
    alpha[fringe] = 0.0
    core = binary_erosion(alpha > 0.5, iterations=1)
    alpha = np.clip(gaussian_filter(np.maximum(alpha, core.astype(np.float64)), 0.7), 0, 1)
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
    return Image.fromarray(rgba, "RGBA")

def export_obj(rgba, key, h=520):
    if rgba.height > h:
        w = max(1, round(rgba.width * h / rgba.height))
        rgba = rgba.resize((w, h), Image.LANCZOS)
    rgba.save(os.path.join(OUT, f"prop_{key}.png"))
    rgba.save(os.path.join(OUT, f"prop_{key}.webp"), quality=82, method=6)

def export_flat(im, name, maxw=2200):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, f"{name}.png"))
    im.save(os.path.join(OUT, f"{name}.webp"), quality=84, method=6)

only = sys.argv[1:]
def want(key, outname):
    if only: return key in only
    return not os.path.exists(os.path.join(OUT, outname))

# ---- 1. ledge with visible top surface ----
if want("ledge", "ledge_top.png"):
    p = ("The attached image is a line-and-wash watercolour painting of a walnut shelf plank seen "
         "dead-on from the front: only the front face is visible. Paint the SAME plank — same warm "
         "walnut colour, same confident sepia grain lines and knots, same watercolour feel — but "
         "seen from very slightly ABOVE eye level, as a person standing in front of a bookcase sees "
         "a shelf below their eye line: along the TOP edge a narrow strip of the plank's flat top "
         "surface is visible, noticeably paler where it catches the light, with the grain running "
         "along its length and a crisp sepia ink line where the top surface meets the front face. "
         "The top surface should take up roughly the upper QUARTER of the plank's height; the front "
         "face fills the rest. The plank runs edge-to-edge across the whole frame horizontally. "
         "Plain pale warm paper background above the plank, nothing else in frame.")
    im = gen([p, LEDGE], "21:9")
    export_flat(im, "ledge_top")
    print("made ledge_top", flush=True)

# ---- 2. wallpaper candidates ----
WALLPAPERS = {
    "wallpaper_damask": (
        "A flat wallpaper panel filling the whole frame edge-to-edge: a traditional Victorian "
        "damask pattern painted in watercolour, TONE-ON-TONE — aged warm cream background with the "
        "damask motifs only a few shades deeper (pale sepia and faded sage), very low contrast, "
        "quiet and faded like an old study wall. Subtle watercolour wash unevenness. No objects, "
        "no border, no vignette, pattern only, repeating evenly across the frame."),
    "wallpaper_stripe": (
        "A flat wallpaper panel filling the whole frame edge-to-edge: a traditional narrow-stripe "
        "Regency wallpaper painted in watercolour, TONE-ON-TONE — aged warm cream ground with "
        "slim vertical stripes only a few shades deeper (faded sepia, occasional very pale sage "
        "pinstripe), very low contrast, quiet and faded like an old study wall. Subtle watercolour "
        "wash unevenness. No objects, no border, no vignette, pattern only."),
}
for key, p in WALLPAPERS.items():
    if want(key, f"{key}.png"):
        im = gen([p], "3:4")
        export_flat(im, key)
        print("made", key, flush=True)

# ---- 3. clutter props ----
for key, (body, aspect) in OBJECTS.items():
    if want(key, f"prop_{key}.png"):
        im = gen([STYLE + body, LAMP], aspect)
        export_obj(cut(im), key)
        print("made prop_" + key, flush=True)

print("done ->", OUT)
