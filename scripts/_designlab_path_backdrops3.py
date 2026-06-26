"""More backdrop styles for the learning path (GPT-image-2). 5 new briefs,
each STRICT: warm-paper ground, motifs in the margins, a wide empty central
lane for the path, pale/low-contrast, single muted accent, no text.
Saves design-lab/assets/path-bg-{key}.png.
Run:  python scripts/_designlab_path_backdrops3.py
"""
import base64, os, sys
from openai import OpenAI

ACCENT = "#368352"
TOPICS = ("a plant cell, a microscope, dividing cells, a human heart with vessels, "
          "a leaf for photosynthesis, bacteria and viruses, a digestive-system outline")

STRICT = (f"STRICT: vertical portrait. Warm off-white paper (#f7f6f4) fills the ENTIRE image. "
          f"Place every motif ONLY in the far-left and far-right margins; the whole central vertical "
          f"third MUST stay completely empty — bare paper, reserved for an overlay. Keep everything "
          f"pale, faded and low-contrast. ABSOLUTELY NO text, words, letters, numbers, labels or "
          f"captions. No frame, no border, no watermark.")

BRIEFS = {
  "watercolour":
    f"Soft loose watercolour washes of {TOPICS} — pale, translucent, bleedy wet-on-wet blobs and gentle "
    f"brush shapes in muted green ({ACCENT}) on warm paper, soft feathered edges, minimal detail, airy. " + STRICT,
  "line":
    f"Elegant minimalist CONTINUOUS single-line drawings of {TOPICS} — each object rendered with one clean "
    f"unbroken thin line, very sparse, generous whitespace, modern and refined, single muted green line "
    f"({ACCENT}) on warm paper, no shading, no fills. " + STRICT,
  "stipple":
    f"Delicate stipple / dotwork illustrations of {TOPICS} — forms built entirely from fine tiny dots "
    f"(pointillism), soft and textural, pale, single muted green ({ACCENT}) on warm paper, no outlines, "
    f"no solid fills. " + STRICT,
  "starmap":
    f"A faint celestial star-map: {TOPICS} drawn as CONSTELLATIONS — small glowing dots joined by thin "
    f"hairline connectors to suggest each shape, like an antique star chart, muted green ({ACCENT}) dots "
    f"and faint lines on warm off-white paper, delicate and sparse. " + STRICT,
  "blueprint":
    f"A pale technical blueprint / schematic of {TOPICS} — fine precise faded green ({ACCENT}) outline "
    f"linework with light measurement ticks and thin guide lines, drafting style, on a VERY pale near-white "
    f"warm ground (keep it LIGHT, not a dark blueprint), low-contrast and clean. " + STRICT,
}


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "design-lab", "assets")
    for key, prompt in BRIEFS.items():
        out_path = os.path.join(out_dir, f"path-bg-{key}.png")
        for model in ("gpt-image-2", "gpt-image-1"):
            try:
                print(f"[{key}] {model} 1024x1536 high…", flush=True)
                r = client.images.generate(model=model, prompt=prompt, size="1024x1536", quality="high")
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(r.data[0].b64_json))
                print(f"[{key}] saved ({os.path.getsize(out_path)//1024} KB) via {model}", flush=True)
                break
            except Exception as e:
                print(f"[{key}] {model} failed: {e}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
