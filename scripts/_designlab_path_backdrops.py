"""Design-lab: generate 3 style prototypes for the learning-path backdrop
(GPT-image-2, gpt-image-1 fallback). One per brief, for Biology Paper 1.

Strict prompts: warm-paper ground, single muted accent, PALE/low-contrast so the
path reads on top, motifs only in the side margins with a wide EMPTY central lane,
and hard no-text constraints (AI text garbles; node labels carry the words).

Saves PNGs into design-lab/assets/ so serve.py (root = worktree) serves them.
Run:  python scripts/_designlab_path_backdrops.py
"""
import base64, os, sys
from openai import OpenAI

ACCENT = "#368352"   # Combined Science / biology green
TOPICS = ("a plant cell, a microscope, dividing cells under magnification, "
          "a human heart with blood vessels, a green leaf for photosynthesis, "
          "bacteria and viruses, a simple digestive-system outline")

STRICT = (f"STRICT COMPOSITION: vertical portrait. A warm off-white paper background "
          f"(hex {('#f7f6f4')}) fills the ENTIRE image. Arrange every drawing ONLY along the "
          f"far-left and far-right margins; the whole central vertical third of the image "
          f"MUST be left completely empty — bare paper, nothing drawn there (it is reserved "
          f"for an overlay). Keep everything very pale, faded, light and low-contrast so it "
          f"can sit quietly behind an overlay. Use a single muted green tone ({ACCENT}) only "
          f"(plus the paper). ABSOLUTELY NO text, no words, no letters, no numbers, no labels, "
          f"no captions, no title anywhere. No frame, no border, no watermark, no signature.")

BRIEFS = {
  "sketch":
    f"A loose hand-drawn field-notebook page: faint, light pen-and-ink line sketches "
    f"(thin lines, NO shading, NO fills) of {TOPICS}, in a scientific margin-doodle style, "
    f"small and sparse and faded, single muted green ink ({ACCENT}) on warm off-white paper. "
    + STRICT,
  "engraving":
    f"An antique scientific engraving plate: finely cross-hatched naturalist illustrations of "
    f"{TOPICS}, Victorian textbook-plate style, elegant but PALE, faded and low-contrast, in a "
    f"muted sepia-green ink ({ACCENT}) on aged warm off-white paper. "
    + STRICT,
  "riso":
    f"A risograph-style duotone illustration: simplified bold flat shapes of {TOPICS}, soft "
    f"overlapping flats with a gentle grainy risograph texture, low-contrast and soft, in two "
    f"tones only — muted green ({ACCENT}) and warm cream. "
    + STRICT,
}


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "design-lab", "assets")
    os.makedirs(out_dir, exist_ok=True)
    for key, prompt in BRIEFS.items():
        out_path = os.path.join(out_dir, f"path-bg-{key}.png")
        done = False
        for model in ("gpt-image-2", "gpt-image-1"):
            try:
                print(f"[{key}] generating with {model} (1024x1536, high)…", flush=True)
                r = client.images.generate(model=model, prompt=prompt, size="1024x1536", quality="high")
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(r.data[0].b64_json))
                print(f"[{key}] saved {out_path} ({os.path.getsize(out_path)//1024} KB) via {model}", flush=True)
                done = True
                break
            except Exception as e:
                print(f"[{key}] {model} failed: {e}", flush=True)
        if not done:
            print(f"[{key}] ALL MODELS FAILED", flush=True)
    print("done")


if __name__ == "__main__":
    main()
