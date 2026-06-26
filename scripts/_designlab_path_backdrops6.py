"""Fill in the remaining styles (blueprint, watercolour, riso) for the two
non-science demo units so every subject has the full toggle set.
Saves design-lab/assets/path-bg-{histusa,macbeth}-{blueprint,watercolour,riso}.png.
Run:  python scripts/_designlab_path_backdrops6.py
"""
import base64, os, sys
from openai import OpenAI

SUBJECTS = {
  "histusa": dict(accent="#5b3776", word="muted purple",
    topics=("a vintage Model-T motor car, a jazz saxophone, a Wall Street stock-ticker with a "
            "crashing share-price graph, the Statue of Liberty, art-deco skyscrapers, a 1920s "
            "gramophone, a dust-bowl farmhouse")),
  "macbeth": dict(accent="#7d3737", word="muted maroon red",
    topics=("a king's crown, a bloodied dagger, three hooded witch silhouettes, a bubbling cauldron, "
            "a Scottish castle on a crag, a perched raven, an empty throne")),
}

def strict():
    return ("STRICT: vertical portrait. Warm off-white paper (#f7f6f4) fills the ENTIRE image. Place every "
            "shape ONLY in the far-left and far-right margins; the whole central vertical third MUST stay "
            "completely empty — bare paper, reserved for an overlay. Keep everything pale, faded and "
            "low-contrast. ABSOLUTELY NO text, words, letters, numbers, labels or captions. No frame, no "
            "border, no watermark.")

def prompt(style, s):
    a, w, t = s["accent"], s["word"], s["topics"]
    if style == "blueprint":
        return (f"A pale technical blueprint / schematic of {t} — fine precise faded {w} ({a}) outline linework "
                f"with light measurement ticks and thin guide lines, drafting style, on a VERY pale near-white "
                f"warm ground (keep it LIGHT, not dark), low-contrast and clean. " + strict())
    if style == "watercolour":
        return (f"Soft loose watercolour washes of {t} — pale, translucent, bleedy wet-on-wet blobs and gentle "
                f"brush shapes in {w} ({a}) on warm paper, soft feathered edges, minimal detail, airy. " + strict())
    return (f"A BOLD FLAT two-colour risograph screen-print: big SIMPLE FLAT SILHOUETTE shapes of {t} — chunky "
            f"solid blocks of colour ONLY. NO outlines, NO line-art, NO detail, NO shading. Grainy halftone "
            f"risograph texture with slight mis-registration. Two flat tones: {w} ({a}) and warm cream. "
            f"Graphic, posterised, minimal. " + strict())


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "design-lab", "assets")
    for skey, s in SUBJECTS.items():
        for style in ("blueprint", "watercolour", "riso"):
            out_path = os.path.join(out_dir, f"path-bg-{skey}-{style}.png")
            for model in ("gpt-image-2", "gpt-image-1"):
                try:
                    print(f"[{skey}-{style}] {model}…", flush=True)
                    r = client.images.generate(model=model, prompt=prompt(style, s), size="1024x1536", quality="high")
                    with open(out_path, "wb") as f:
                        f.write(base64.b64decode(r.data[0].b64_json))
                    print(f"[{skey}-{style}] saved ({os.path.getsize(out_path)//1024} KB)", flush=True)
                    break
                except Exception as e:
                    print(f"[{skey}-{style}] {model} failed: {e}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
