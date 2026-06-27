"""Proof-of-concept for Tom's progressive-fidelity idea (27 Jun 2026):
a unit's backdrop sharpens as the student masters it.
Generates the 3 higher stages (blueprint / refined / photo) for ONE flagship
unit — Combined Science · Biology Paper 2 (the DNA unit). Stage 0 (sketch) is
made by _designlab_unit_backdrops.py.

Files: path-bg-u-science-aqa-biology-paper-2-{blueprint,refined,photo}.png
Run:   python scripts/_designlab_fidelity_ladder.py
"""
import base64, os, sys
from openai import OpenAI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")

SUBJECT = "science-aqa"; UNIT = "biology-paper-2"
ACCENT = "#368352"; WORD = "muted green"
MOTIFS = ("a DNA double helix, a branching neuron, a side profile of a brain, a Punnett inheritance "
          "square, an eye, a kidney, a simple food chain of creatures")

CORE = ("vertical portrait. Warm off-white paper (#f7f6f4) is the background. Place every object ONLY in "
        "the far-left and far-right margins; the whole central vertical third MUST stay completely empty — "
        "bare paper, reserved for an overlay. ABSOLUTELY NO text, words, letters, numbers, labels or "
        "captions. No frame, no border, no watermark.")

PROMPTS = {
 "blueprint": (f"A precise technical BLUEPRINT / schematic of {MOTIFS} — clean confident {WORD} ({ACCENT}) "
               f"outline linework with light measurement ticks and thin construction guide-lines, drafting "
               f"style, more complete and assured than a rough sketch but still line-only on pale warm paper, "
               f"low-contrast. STRICT: " + CORE),
 "refined": (f"A beautifully RENDERED, detailed pen-and-ink and soft-watercolour illustration of {MOTIFS} — "
             f"confident finished linework with gentle {WORD} ({ACCENT}) washes, light shading and texture, "
             f"a polished naturalist's notebook plate, richer and more finished than a blueprint but still "
             f"calm and not too dark. STRICT: " + CORE),
 "photo": (f"Richly detailed, PHOTOREALISTIC full-colour renderings of {MOTIFS} — lifelike texture, depth, "
           f"soft studio lighting and shading, like high-quality photographs of each object, vivid and "
           f"fully resolved (this is the finished reward state). Keep them tasteful and arranged in the "
           f"margins. STRICT: " + CORE),
}

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI()
    for stage, prompt in PROMPTS.items():
        out = os.path.join(ASSETS, f"path-bg-u-{SUBJECT}-{UNIT}-{stage}.png")
        if os.path.exists(out) and os.path.getsize(out) > 20000:
            print(f"[{stage}] exists, skip", flush=True); continue
        for model in ("gpt-image-2", "gpt-image-1"):
            try:
                print(f"[{stage}] {model}…", flush=True)
                r = client.images.generate(model=model, prompt=prompt, size="1024x1536", quality="high")
                with open(out, "wb") as f:
                    f.write(base64.b64decode(r.data[0].b64_json))
                print(f"[{stage}] saved ({os.path.getsize(out)//1024} KB)", flush=True); break
            except Exception as e:
                print(f"[{stage}] {model} failed: {e}", flush=True)
    print("done")

if __name__ == "__main__":
    main()
