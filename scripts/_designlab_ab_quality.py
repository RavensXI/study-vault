"""A/B: generate the same Biology Paper 1 backdrop at HIGH vs MEDIUM quality,
for both the sketch (generate) and the photoreal (img2img edit), so we can judge
whether medium is good enough before a full-site rollout.
Writes design-lab/assets/_ab-{sketch,photo}-{high,medium}.png
"""
import base64, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import MOTIFS, ACCENT, sketch_prompt
from _designlab_aligned_ladder import prompts as ladder_prompts
from openai import OpenAI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
SUBJECT, UNIT = "science-aqa", "biology-paper-1"
hexc, word = ACCENT[SUBJECT]
motifs = MOTIFS[f"{SUBJECT}/{UNIT}"]
sketch_in = os.path.join(ASSETS, f"path-bg-u-{SUBJECT}-{UNIT}.png")   # existing sketch = img2img source

def save(path, b64):
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))
    return os.path.getsize(path) // 1024

def main():
    c = OpenAI()
    sp = sketch_prompt(motifs, word, hexc)
    pp = ladder_prompts(motifs, word, hexc)["photo"]
    for q in ("high", "medium"):
        # sketch (text->image)
        out = os.path.join(ASSETS, f"_ab-sketch-{q}.png")
        try:
            print(f"[sketch {q}]…", flush=True)
            r = c.images.generate(model="gpt-image-2", prompt=sp, size="1024x1536", quality=q)
            print(f"[sketch {q}] saved {save(out, r.data[0].b64_json)} KB", flush=True)
        except Exception as e:
            print(f"[sketch {q}] FAIL {str(e)[:160]}", flush=True)
        # photo (img2img edit from the existing sketch)
        out = os.path.join(ASSETS, f"_ab-photo-{q}.png")
        try:
            print(f"[photo {q}]…", flush=True)
            with open(sketch_in, "rb") as img:
                r = c.images.edit(model="gpt-image-2", image=img, prompt=pp, size="1024x1536", quality=q)
            print(f"[photo {q}] saved {save(out, r.data[0].b64_json)} KB", flush=True)
        except Exception as e:
            print(f"[photo {q}] FAIL {str(e)[:160]}", flush=True)
    print("done")

if __name__ == "__main__":
    main()
