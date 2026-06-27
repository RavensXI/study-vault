"""Aligned fidelity ladder via IMAGE-TO-IMAGE: each higher state is generated
FROM the unit's sketch (images.edit), so the SAME objects stay in the SAME
positions and only the rendering sharpens — sketch → blueprint → refined → photo.
This makes the in-place transition clean (a microscope sharpening, not a morph).

Input:  design-lab/assets/path-bg-u-<subject>-<unit>.png  (the sketch, stage 0)
Output: ...-blueprint.png / ...-refined.png / ...-photo.png  (composition-locked)

Usage: python scripts/_designlab_aligned_ladder.py <subject> <unit-slug>
Example: python scripts/_designlab_aligned_ladder.py science-aqa biology-paper-1
"""
import base64, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import ACCENT
from openai import OpenAI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")

KEEP = ("Keep the SAME objects in the EXACT SAME positions, same sizes and the same composition as the input. "
        "Keep the warm off-white paper and the empty central vertical third completely empty (no objects there). "
        "ABSOLUTELY NO text, words, letters, numbers or labels.")

def prompts(word, hexc):
    return {
      "blueprint": (f"Redraw this exact image as a precise technical BLUEPRINT: render every shape as clean confident "
                    f"{word} ({hexc}) outline linework with light measurement ticks and thin construction guide-lines, "
                    f"drafting style, on pale warm paper. {KEEP}"),
      "refined":   (f"Redraw this exact image as a detailed PEN-AND-INK and soft-watercolour illustration: confident "
                    f"finished linework with gentle {word} ({hexc}) washes, light shading and texture, a polished "
                    f"naturalist's notebook plate, calm and not too dark. {KEEP}"),
      "photo":     (f"Transform this exact sketch into a richly detailed PHOTOREALISTIC version: each object becomes a "
                    f"lifelike, full-colour photograph with real texture, depth and soft studio lighting, vivid and "
                    f"fully resolved. {KEEP}"),
    }

def main():
    if len(sys.argv) < 3:
        sys.exit("usage: <subject> <unit-slug>")
    subject, unit = sys.argv[1], sys.argv[2]
    hexc, word = ACCENT[subject]
    sketch = os.path.join(ASSETS, f"path-bg-u-{subject}-{unit}.png")
    if not os.path.exists(sketch):
        sys.exit(f"sketch not found: {sketch} (generate it with _designlab_unit_backdrops.py first)")
    client = OpenAI()
    for stage, prompt in prompts(word, hexc).items():
        out = os.path.join(ASSETS, f"path-bg-u-{subject}-{unit}-{stage}.png")
        ok = False
        for model in ("gpt-image-2", "gpt-image-1"):
            try:
                print(f"[{stage}] {model} edit…", flush=True)
                with open(sketch, "rb") as img:
                    r = client.images.edit(model=model, image=img, prompt=prompt, size="1024x1536")
                b64 = r.data[0].b64_json
                with open(out, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"[{stage}] saved ({os.path.getsize(out)//1024} KB) via {model}", flush=True)
                ok = True; break
            except Exception as e:
                print(f"[{stage}] {model} failed: {str(e)[:160]}", flush=True)
        if not ok:
            print(f"[{stage}] all models failed", flush=True)
    print("done")

if __name__ == "__main__":
    main()
