"""Regenerate two backdrop styles with harder prompts:
- sketch: ROUGH, loose, unfinished gestural doodles (was too polished)
- riso:   FLAT bold duotone silhouettes, no linework (was ~ engraving)
Overwrites design-lab/assets/path-bg-{sketch,riso}.png. Engraving left as-is.
Run:  python scripts/_designlab_path_backdrops2.py
"""
import base64, os, sys
from openai import OpenAI

ACCENT = "#368352"
TOPICS = ("a plant cell, a microscope, dividing cells, a human heart with vessels, "
          "a leaf for photosynthesis, bacteria and viruses, a digestive-system outline")

STRICT = (f"STRICT: vertical portrait. Warm off-white paper (#f7f6f4) fills the ENTIRE image. "
          f"Put every shape ONLY in the far-left and far-right margins; the whole central vertical "
          f"third MUST stay completely empty (bare paper, reserved for an overlay). Keep it pale, "
          f"faded and low-contrast. ABSOLUTELY NO text, words, letters, numbers, labels or captions. "
          f"No frame, no border, no watermark.")

BRIEFS = {
  "sketch":
    f"VERY ROUGH, loose, UNFINISHED hand-sketch — quick scratchy biro/pencil doodles of {TOPICS}, "
    f"drawn fast and imperfectly: wobbly lines, visible construction marks, several shapes only "
    f"HALF-DRAWN or suggested with a couple of strokes, sparse, gestural, messy, incomplete — like "
    f"10-second margin scribbles, NOT a finished or detailed drawing. Thin faint single muted-green "
    f"line ({ACCENT}) on warm paper, no shading, no fills. " + STRICT,
  "riso":
    f"A BOLD FLAT two-colour risograph screen-print: big SIMPLE FLAT SILHOUETTE shapes of {TOPICS} — "
    f"chunky solid blocks of colour ONLY. NO outlines, NO line-art, NO cross-hatching, NO fine detail, "
    f"NO shading, NO realism. Grainy halftone risograph texture with slight colour mis-registration. "
    f"Exactly two flat tones: muted green ({ACCENT}) and warm cream. Graphic, posterised, minimal, "
    f"simplified like cut-paper. " + STRICT,
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
