"""Build ONE unit's long thin NON-REPEATING banner for the V2 lane:
  panorama (21:9) -> outpaint-EXTEND rightward k times with fresh motifs ->
  blend-stitch the segments with an overlap crossfade -> write -land.png.

The centre band is deliberately kept EMPTY (no painted path/road/river) — the
learning-path nodes are superimposed by the app on top.

Usage: python scripts/_designlab_strip.py <subject> <unit-slug> [n_lessons]
       (n_lessons sets how many extend segments are needed to cover the lane)
Env:   DL_GEMINI_MODEL (default gemini-3-pro-image-preview)
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import ACCENT
from _designlab_aligned_ladder import motifs_for
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
try:
    BG_MANIFEST = json.load(open(os.path.join(ROOT, "design-lab", "_path_backdrops.json"), encoding="utf-8"))
except Exception:
    BG_MANIFEST = {}

def unit_name_for(skey, slug):
    m = BG_MANIFEST.get(f"{skey}/{slug}")
    return (m or {}).get("name") or slug.replace("-", " ")
MODEL = os.environ.get("DL_GEMINI_MODEL", "gemini-3-pro-image-preview")
MAX_EXTENDS = int(os.environ.get("DL_MAX_EXTENDS", "1"))   # the model reliably invents ONE fresh set; 2+ drifts back to repeats
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# lane geometry must mirror dashboard-paths-v2.html renderLane()
LANE_H, PAD_L, GAP_X = 264, 78, 124
PANO_ASPECT = 21/9                 # widest native single image
OVERLAP = 140                      # px crossfade between stitched segments (at native height)

NOPATH = ("Do NOT draw any path, road, river, ribbon, line or trail. ABSOLUTELY NO text, words, "
          "letters, numbers or labels anywhere.")

def extract(resp):
    for cand in (resp.candidates or []):
        for part in (cand.content.parts or []):
            d = getattr(part, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(contents, out):
    cfgs = [types.GenerateContentConfig(response_modalities=["IMAGE"],
                                        image_config=types.ImageConfig(aspect_ratio="21:9")),
            types.GenerateContentConfig(response_modalities=["IMAGE"])]
    for cfg in cfgs:
        try:
            resp = client.models.generate_content(model=MODEL, contents=contents, config=cfg)
            data = extract(resp)
            if data:
                open(out, "wb").write(data)
                return out
        except Exception as e:
            print(f"   gen err: {str(e)[:140]}", flush=True)
    return None

def n_extends_for(n_lessons):
    lesson_w = PAD_L * 2 + max(0, n_lessons - 1) * GAP_X
    target_aspect = lesson_w / LANE_H
    pano = PANO_ASPECT
    per_extend = PANO_ASPECT - OVERLAP / LANE_H      # added aspect per extra segment
    return max(0, math.ceil((target_aspect - pano) / per_extend))

def stitch(imgs):
    H = min(im.height for im in imgs)
    imgs = [im.resize((round(im.width * H / im.height), H)) for im in imgs]
    total = imgs[0].width + sum(im.width - OVERLAP for im in imgs[1:])
    canvas = Image.new("RGB", (total, H), "#f6f2ea")
    canvas.paste(imgs[0], (0, 0)); x = imgs[0].width
    for im in imgs[1:]:
        mask = Image.new("L", (im.width, H), 255); px = mask.load()
        for xx in range(OVERLAP):
            v = int(255 * xx / OVERLAP)
            for yy in range(H):
                px[xx, yy] = v
        canvas.paste(im, (x - OVERLAP, 0), mask); x += im.width - OVERLAP
    return canvas

def build(skey, slug, n_lessons):
    motifs = motifs_for(skey, slug)
    uname = unit_name_for(skey, slug)
    k = min(MAX_EXTENDS, n_extends_for(n_lessons))
    tmp = os.path.join(ASSETS, f"_strip-{skey}-{slug}")
    style = ("Render it as ONE cohesive modern editorial SCREEN-PRINT illustration in a single unified style and a "
             "limited palette of sage green, warm cream and deep ink: bold clean contour linework, every element "
             "drawn the same way and connected by flowing lines into one seamless woven composition that fills the "
             "whole banner top to bottom — a tapestry of ideas. NOT separate cut-out objects, NOT a collage, NOT "
             "photographs, NO empty bands. Warm off-white paper. ABSOLUTELY NO text, letters, numbers or labels.")
    pano_prompt = (f"A wide horizontal banner weaving these GCSE \"{uname}\" ideas together into one continuous "
                   f"illustrated scene: {motifs}. {style}")
    print(f"[{skey}/{slug}] {n_lessons} lessons -> {k} extend(s) (D tapestry)", flush=True)
    p0 = gen([pano_prompt], tmp + "-0.png")   # text-to-image keeps it cohesive (no isolated-object source to copy)
    if not p0:
        print("   panorama failed", flush=True); return False
    segs = [Image.open(p0).convert("RGB")]
    for i in range(k):
        ext_prompt = (f"Continue this illustration to the RIGHT as ONE seamless mural in EXACTLY the same style and "
                      f"palette. Weave in a COMPLETELY DIFFERENT set of \"{uname}\" ideas — do NOT repeat any of "
                      f"these: {motifs}. The far-left edge of your image must continue smoothly from this picture. "
                      f"{style}")
        pi = gen([ext_prompt, segs[-1]], tmp + f"-{i+1}.png")
        if not pi:
            print(f"   extend {i+1} failed, stopping early", flush=True); break
        segs.append(Image.open(pi).convert("RGB"))
    # complete = the canonical composition; refined + sketch are ALIGNED transforms of the SAME segments
    keep = ("Keep the SAME composition — every element in the SAME position and size as the input image. "
            "ABSOLUTELY NO text, letters or numbers.")
    stage_prompts = {
        "refined": ("Redraw this exact image as a REFINED line-illustration stage: confident clean single-weight "
                    "deep-sage contour linework on warm paper with only the faintest hint of flat colour, mostly "
                    "uncoloured — the inked stage just before the finished print. " + keep),
        "sketch":  ("Redraw this exact image as a loose hand-drawn PENCIL SKETCH: rough, light, unfinished graphite "
                    "linework on warm paper, no colour, the look of a quick first study. " + keep),
    }
    def out_for(stage):
        suf = "land.png" if stage == "sketch" else f"land-{stage}.png"   # sketch=base; complete saved to -photo slot
        return os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}-{suf}")
    stitch(segs).save(out_for("photo")); made = ["complete"]
    for stage, prompt in stage_prompts.items():
        tsegs, ok = [], True
        for si, seg in enumerate(segs):
            tp = gen([prompt, seg], tmp + f"-{stage}-{si}.png")
            if not tp:
                ok = False; break
            tsegs.append(Image.open(tp).convert("RGB"))
        if ok and tsegs:
            stitch(tsegs).save(out_for(stage)); made.append(stage)
        else:
            print(f"   {stage} failed", flush=True)
    import glob
    for f in glob.glob(tmp + "*.png"):
        try: os.remove(f)
        except OSError: pass
    print(f"   saved stages: {', '.join(made)}", flush=True)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: <subject> <unit-slug> [n_lessons]")
    build(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 10)
