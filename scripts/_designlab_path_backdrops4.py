"""Backdrop style: a blend of SKETCH + BLUEPRINT — a rough hand-drawn technical
sketch (loose gestural drawings overlaid with faint drafting guide-lines, a
light grid and measurement ticks). Saves design-lab/assets/path-bg-draft.png.
Run:  python scripts/_designlab_path_backdrops4.py
"""
import base64, os, sys
from openai import OpenAI

ACCENT = "#368352"
TOPICS = ("a plant cell, a microscope, dividing cells, a human heart with vessels, "
          "a leaf for photosynthesis, bacteria and viruses, a digestive-system outline")

STRICT = (f"STRICT: vertical portrait. Warm off-white paper (#f7f6f4) fills the ENTIRE image. "
          f"Place every drawing ONLY in the far-left and far-right margins; the whole central "
          f"vertical third MUST stay completely empty — bare paper, reserved for an overlay. Keep "
          f"everything pale, faded and low-contrast. ABSOLUTELY NO text, words, letters, numbers, "
          f"labels or captions. No frame, no border, no watermark.")

PROMPT = (
    f"A rough hand-drawn TECHNICAL field-sketch — loose, gestural, slightly scratchy biro/pencil "
    f"drawings of {TOPICS} (imperfect, wobbly lines, some shapes only half-drawn), OVERLAID with light "
    f"technical scaffolding: faint thin construction guide-lines, a subtle drafting grid, small "
    f"measurement ticks, dimension arrows and a stray compass/protractor arc here and there — like a "
    f"rough engineer's or naturalist's working notebook that mixes quick sketches with blueprint-style "
    f"guides. Single muted green ink ({ACCENT}) on warm paper, no shading, no fills, hand-drawn and "
    f"unfinished but with technical guides. " + STRICT)


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "design-lab", "assets")
    out_path = os.path.join(out_dir, "path-bg-draft.png")
    for model in ("gpt-image-2", "gpt-image-1"):
        try:
            print(f"[draft] {model} 1024x1536 high…", flush=True)
            r = client.images.generate(model=model, prompt=PROMPT, size="1024x1536", quality="high")
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(r.data[0].b64_json))
            print(f"[draft] saved ({os.path.getsize(out_path)//1024} KB) via {model}", flush=True)
            break
        except Exception as e:
            print(f"[draft] {model} failed: {e}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
