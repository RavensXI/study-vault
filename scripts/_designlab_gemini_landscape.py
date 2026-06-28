"""Generate WIDE landscape banner backdrops for the V2 carousel prototype.

For each of SAM's units, recompose its existing (portrait) backdrop into a wide
16:9 horizontal banner with a clear central horizontal lane, so a left-to-right
lesson trail can run across it. Source = best available fidelity (photo > refined
> blueprint > sketch). Output: design-lab/assets/path-bg-u-<skey>-<slug>-land.png

Idempotent (skips files already on disk). Subjects ordered so the strong demo
subjects (Combined Science, Maths) generate first.

Run:  python scripts/_designlab_gemini_landscape.py            (all SAM units)
      python scripts/_designlab_gemini_landscape.py science-aqa (one subject)
Env:  DL_GEMINI_MODEL (default gemini-3-pro-image-preview = Nano Banana Pro)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import ACCENT
from _designlab_aligned_ladder import motifs_for
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
UNITS = json.load(open(os.path.join(ROOT, "scratch_sam_units.json"), encoding="utf-8"))
MODEL = os.environ.get("DL_GEMINI_MODEL", "gemini-3-pro-image-preview")
ORDER_FIRST = ["science-aqa", "maths-ocr", "history-ocr", "geography-edexcel-b"]

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

CFGS = [types.GenerateContentConfig(response_modalities=["IMAGE"],
                                    image_config=types.ImageConfig(aspect_ratio="16:9")),
        types.GenerateContentConfig(response_modalities=["IMAGE"]), None]

def extract(resp):
    for cand in (resp.candidates or []):
        for part in (cand.content.parts or []):
            d = getattr(part, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def source_for(skey, slug):
    base = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}")
    for stage in ("-photo", "-refined", "-blueprint", ""):
        p = f"{base}{stage}.png"
        if os.path.exists(p) and os.path.getsize(p) > 20000:
            return p
    return None

def prompt_for(skey, slug):
    hexc, word = ACCENT[skey]
    motifs = motifs_for(skey, slug)
    return (
        f"Recompose this picture as a WIDE cinematic horizontal banner (landscape). "
        f"Use the SAME subjects and motifs — the drawing depicts these specific things: {motifs}; "
        f"render each as exactly what it is meant to be, do NOT reinterpret any shape as a different object. "
        f"Spread the detailed motifs along the TOP edge and the BOTTOM edge of the banner, and keep the "
        f"HORIZONTAL MIDDLE BAND calm, open and uncluttered (soft warm off-white paper / quiet ground) so a "
        f"winding trail can run left-to-right across the middle. Richly detailed, full colour, soft natural "
        f"light, gentle {word} ({hexc}) tones, warm paper texture. "
        f"ABSOLUTELY NO text, words, letters, numbers or labels."
    )

def gen(src_img, prompt, out, label):
    for attempt in range(5):
        for cfg in CFGS:
            try:
                kw = {"model": MODEL, "contents": [prompt, src_img]}
                if cfg is not None:
                    kw["config"] = cfg
                resp = client.models.generate_content(**kw)
                data = extract(resp)
                if data:
                    with open(out, "wb") as f:
                        f.write(data)
                    print(f"  [{label}] saved ({os.path.getsize(out)//1024} KB)", flush=True)
                    return True
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("RESOURCE_EXHAUSTED", "429", "quota", "rate")):
                    wait = 8 * (attempt + 1)
                    print(f"  [{label}] rate-limited, waiting {wait}s…", flush=True)
                    time.sleep(wait); break
                print(f"  [{label}] error: {msg[:150]}", flush=True)
        else:
            continue
    print(f"  [{label}] FAILED", flush=True)
    return False

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    keys = list(UNITS.keys())
    keys.sort(key=lambda k: (ORDER_FIRST.index(k) if k in ORDER_FIRST else len(ORDER_FIRST)))
    made = skipped = failed = nosrc = 0
    for skey in keys:
        if only and skey != only:
            continue
        for u in UNITS[skey]["units"]:
            slug = u["slug"]
            out = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}-land.png")
            if os.path.exists(out) and os.path.getsize(out) > 20000:
                skipped += 1; continue
            src = source_for(skey, slug)
            if not src:
                print(f"[{skey}/{slug}] no source art, skip", flush=True); nosrc += 1; continue
            print(f"[{skey}/{slug}] from {os.path.basename(src)}", flush=True)
            if gen(Image.open(src), prompt_for(skey, slug), out, f"{skey}/{slug}"):
                made += 1
            else:
                failed += 1
    print(f"\ndone — made {made}, skipped {skipped}, failed {failed}, no-source {nosrc}", flush=True)

if __name__ == "__main__":
    main()
