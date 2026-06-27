"""Generate the aligned fidelity ladder (blueprint / refined / photo) for SAM's
units via Google Gemini (Nano Banana Pro), img2img from each unit's existing
sketch. Motif-aware (tells the model what each shape is) and idempotent
(skips stages already on disk, so it resumes after rate-limits).

Run:  python scripts/_designlab_gemini_ladder.py            (all SAM units)
      python scripts/_designlab_gemini_ladder.py science-aqa (one subject)
Env:  DL_GEMINI_MODEL (default gemini-3-pro-image-preview = Nano Banana Pro)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import ACCENT
from _designlab_aligned_ladder import prompts as ladder_prompts, motifs_for
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
UNITS = json.load(open(os.path.join(ROOT, "scratch_sam_units.json"), encoding="utf-8"))
MODEL = os.environ.get("DL_GEMINI_MODEL", "gemini-3-pro-image-preview")
STAGES = ("blueprint", "refined", "photo")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def extract(resp):
    for cand in (resp.candidates or []):
        for part in (cand.content.parts or []):
            d = getattr(part, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

CFGS = [types.GenerateContentConfig(response_modalities=["IMAGE"],
                                    image_config=types.ImageConfig(aspect_ratio="2:3")),
        types.GenerateContentConfig(response_modalities=["IMAGE"]), None]

def edit(sketch_img, prompt, out, label):
    for attempt in range(5):
        for cfg in CFGS:
            try:
                kw = {"model": MODEL, "contents": [prompt, sketch_img]}
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
                    time.sleep(wait)
                    break  # retry outer loop
                print(f"  [{label}] error: {msg[:140]}", flush=True)
        else:
            continue
    print(f"  [{label}] FAILED after retries", flush=True)
    return False

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    made = skipped = failed = nosketch = 0
    for skey, sub in UNITS.items():
        if only and skey != only:
            continue
        hexc, word = ACCENT[skey]
        for u in sub["units"]:
            slug = u["slug"]
            sketch_path = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}.png")
            if not os.path.exists(sketch_path):
                print(f"[{skey}/{slug}] no sketch, skip", flush=True); nosketch += 1; continue
            prompts = ladder_prompts(motifs_for(skey, slug), word, hexc)
            sketch_img = Image.open(sketch_path)
            print(f"[{skey}/{slug}]", flush=True)
            for stage in STAGES:
                out = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}-{stage}.png")
                if os.path.exists(out) and os.path.getsize(out) > 20000:
                    skipped += 1; continue
                if edit(sketch_img, prompts[stage], out, stage):
                    made += 1
                else:
                    failed += 1
    print(f"\ndone — made {made}, skipped {skipped}, failed {failed}, no-sketch {nosketch}", flush=True)

if __name__ == "__main__":
    main()
