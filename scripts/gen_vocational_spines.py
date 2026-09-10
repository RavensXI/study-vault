# -*- coding: utf-8 -*-
"""Paint the 12 vocational spines missing from assets/lw/shelf/ in the same
line-and-wash hand as the 34 originals, via gpt-image-2.5-sunburst with two of
the originals as reference images. Cut to alpha, defringed, exported at the
originals' 650px height (webp). Logs token usage per image to _spines_log.json.
Run: python scripts/gen_vocational_spines.py [key ...]  (spines land in assets/lw/shelf/)"""
import io, os, sys, json, base64, time, requests
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, gaussian_filter, label as cclabel

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "assets", "lw", "shelf")
KEY = os.environ["OPENAI_API_KEY"]
LOG = os.path.join(HERE, "_spines_log.json")

# key -> (title, cloth, hex, second reference spine)
ROSTER = {
    "child-development":      ("CHILD DEVELOPMENT",       "soft teal-green cloth",     "#4e7d78", "hsc"),
    "creative-imedia":        ("CREATIVE iMEDIA",         "coral-orange cloth",        "#c46a4a", "spanish"),
    "engineering-design":     ("ENGINEERING DESIGN",      "slate-blue cloth",          "#4f6178", "cs"),
    "engineering-manufacture":("ENGINEERING MANUFACTURE", "steel-grey cloth",          "#5a6068", "eng"),
    "programmable-systems":   ("PROGRAMMABLE SYSTEMS",    "dark teal-blue cloth",      "#3d5f6e", "music"),
    "enterprise-marketing":   ("ENTERPRISE & MARKETING",  "warm mustard cloth",        "#a8842f", "food"),
    "sport-science":          ("SPORT SCIENCE",           "brick-red cloth",           "#a34a3a", "pe"),
    "sport-studies":          ("SPORT STUDIES",           "muted orange-red cloth",    "#b0573c", "pe"),
    "construction":           ("CONSTRUCTION",            "ochre-brown cloth",         "#8a713b", "dt"),
    "ict":                    ("ICT",                     "cool blue-grey cloth",      "#4f6d7d", "it"),
    "retail-business":        ("RETAIL BUSINESS",         "navy cloth",                "#3f5570", "business"),
    "sport-coaching":         ("SPORT & COACHING",        "olive-green cloth",         "#6d7a4e", "geog"),
}
PAPER = (246, 241, 231)


def ref_png(key):
    im = Image.open(os.path.join(OUT, f"book_{key}.webp")).convert("RGBA")
    # centre the spine on a tall paper sheet at the model's aspect
    W, H = 1024, 1536
    scale = (H * 0.86) / im.height
    im = im.resize((max(1, round(im.width * scale)), round(im.height * scale)), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), PAPER + (255,))
    bg.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2))
    b = io.BytesIO(); bg.convert("RGB").save(b, "PNG"); return b.getvalue()


def prompt_for(title, desc, hexc):
    spelled = " ".join(list(title.replace(" ", "␣")))
    return ("The attached images are finished paintings of cloth hardback books seen square-on from the SPINE: "
            "clean pen-and-ink linework with thin watercolour washes, raised bands, and a gold gilt serif title "
            "running top-to-bottom down the spine, on plain pale warm paper. Paint ONE MORE book in exactly this "
            f"hand and format: the cloth painted {desc} (close to {hexc}); the same proportions, bands and gilt "
            f"rules; the spine title '{title}' in the SAME vertical gold gilt serif capitals, running top-to-bottom, "
            "fitted to the spine (a second column of lettering if the words are long, like a real bound book, never "
            "splitting a word). No label panel: the gilt sits directly on the cloth. "
            f"Spell the title EXACTLY, letter by letter: {spelled} - no other words anywhere. "
            "Exactly one book, standing alone, filling most of the frame height, plain pale warm paper background "
            "(#f6f1e7), nothing else in frame.")


def gen(key, title, desc, hexc, ref2, quality="medium"):
    files = [("image[]", ("history.png", ref_png("history"), "image/png")),
             ("image[]", (ref2 + ".png", ref_png(ref2), "image/png"))]
    data = {"model": "gpt-image-2.5-sunburst", "prompt": prompt_for(title, desc, hexc),
            "quality": quality, "size": "1024x1536", "n": "1", "output_format": "png"}
    for attempt in range(3):
        r = requests.post("https://api.openai.com/v1/images/edits", headers={"Authorization": "Bearer " + KEY},
                          files=files, data=data, timeout=600)
        if r.status_code == 200:
            j = r.json(); u = j.get("usage", {})
            return Image.open(io.BytesIO(base64.b64decode(j["data"][0]["b64_json"]))).convert("RGB"), u
        print("  retry", attempt, r.status_code, r.text[:200], flush=True); time.sleep(8)
    raise RuntimeError("gen failed " + key)


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


def export(rgba, key):
    h = 650; w = max(1, round(rgba.width * h / rgba.height))
    small = rgba.resize((w, h), Image.LANCZOS)
    small.save(os.path.join(OUT, f"book_{key}.webp"), quality=82, method=6)
    return w


log = json.load(open(LOG)) if os.path.exists(LOG) else {}
only = sys.argv[1:]
for key, (title, desc, hexc, ref2) in ROSTER.items():
    if only and key not in only: continue
    p = os.path.join(OUT, f"book_{key}.webp")
    if os.path.exists(p) and not only:
        print("have", key, flush=True); continue
    t0 = time.time()
    im, usage = gen(key, title, desc, hexc, ref2)
    raw = os.path.join(os.path.dirname(HERE), "_spines_raw"); os.makedirs(raw, exist_ok=True)
    im.save(os.path.join(raw, f"{key}.png"))
    w = export(cut(im), key)
    it = usage.get("input_tokens", 0); ot = usage.get("output_tokens", 0)
    cost = (usage.get("input_tokens_details", {}).get("text_tokens", 0) * 5 + usage.get("input_tokens_details", {}).get("image_tokens", 0) * 8 + ot * 30) / 1e6
    log[key] = {"title": title, "input_tokens": it, "output_tokens": ot, "usd": round(cost, 4), "width": w, "secs": round(time.time() - t0)}
    json.dump(log, open(LOG, "w"), indent=1)
    print("made", key, "->", title, f"{w}px wide", f"${cost:.3f}", flush=True)
print("done; total $%.3f" % sum(v["usd"] for v in log.values()))
