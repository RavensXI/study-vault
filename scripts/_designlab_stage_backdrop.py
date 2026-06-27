"""Generate a single higher-fidelity stage backdrop for one unit (reusable for
the progressive-fidelity rollout). Pulls motifs/accent from the sketch generator.

Usage: python scripts/_designlab_stage_backdrop.py <subject> <unit-slug> <stage>[ ...more triples]
       stage in {blueprint, refined, photo}
Example: python scripts/_designlab_stage_backdrop.py science-aqa biology-paper-1 photo science-aqa chemistry-paper-1 blueprint
"""
import base64, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import MOTIFS, ACCENT, fallback_motifs, UNITS
from openai import OpenAI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")

CORE = ("vertical portrait. Warm off-white paper (#f7f6f4) is the background. Place every object ONLY in "
        "the far-left and far-right margins; the whole central vertical third MUST stay completely empty — "
        "bare paper, reserved for an overlay. ABSOLUTELY NO text, words, letters, numbers, labels or "
        "captions. No frame, no border, no watermark.")

def prompt(stage, motifs, word, hexc):
    if stage == "blueprint":
        return (f"A precise technical BLUEPRINT / schematic of {motifs} — clean confident {word} ({hexc}) "
                f"outline linework with light measurement ticks and thin construction guide-lines, drafting "
                f"style, more complete and assured than a rough sketch but still line-only on pale warm paper, "
                f"low-contrast. STRICT: " + CORE)
    if stage == "refined":
        return (f"A beautifully RENDERED, detailed pen-and-ink and soft-watercolour illustration of {motifs} — "
                f"confident finished linework with gentle {word} ({hexc}) washes, light shading and texture, a "
                f"polished naturalist's notebook plate, richer and more finished than a blueprint but still calm "
                f"and not too dark. STRICT: " + CORE)
    return (f"Richly detailed, PHOTOREALISTIC full-colour renderings of {motifs} — lifelike texture, depth, soft "
            f"studio lighting and shading, like high-quality photographs of each object, vivid and fully resolved "
            f"(the finished reward state). Tasteful, arranged in the margins. STRICT: " + CORE)

def motifs_for(subject, unit):
    key = f"{subject}/{unit}"
    if key in MOTIFS:
        return MOTIFS[key]
    for u in UNITS.get(subject, {}).get("units", []):
        if u["slug"] == unit:
            return fallback_motifs(u)
    return unit.replace("-", " ")

def main():
    args = sys.argv[1:]
    if len(args) < 3 or len(args) % 3:
        sys.exit("need triples: <subject> <unit> <stage> ...")
    client = OpenAI()
    for i in range(0, len(args), 3):
        subject, unit, stage = args[i], args[i+1], args[i+2]
        hexc, word = ACCENT[subject]
        out = os.path.join(ASSETS, f"path-bg-u-{subject}-{unit}-{stage}.png")
        if os.path.exists(out) and os.path.getsize(out) > 20000:
            print(f"[{subject}/{unit}/{stage}] exists, skip", flush=True); continue
        p = prompt(stage, motifs_for(subject, unit), word, hexc)
        for model in ("gpt-image-2", "gpt-image-1"):
            try:
                print(f"[{subject}/{unit}/{stage}] {model}…", flush=True)
                r = client.images.generate(model=model, prompt=p, size="1024x1536", quality="high")
                with open(out, "wb") as f:
                    f.write(base64.b64decode(r.data[0].b64_json))
                print(f"[{subject}/{unit}/{stage}] saved ({os.path.getsize(out)//1024} KB)", flush=True); break
            except Exception as e:
                print(f"[{subject}/{unit}/{stage}] {model} failed: {e}", flush=True)
    print("done")

if __name__ == "__main__":
    main()
