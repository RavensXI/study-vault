"""Backdrops for two non-science units (to prove the style generalises):
  History  -> "The USA 1919-1948" (accent #5b3776, muted purple)
  Eng Lit  -> "Macbeth"            (accent #7d3737, muted maroon)
Each in two styles: sketch (rough doodles) + draft (sketch x blueprint blend).
Saves design-lab/assets/path-bg-{histusa,macbeth}-{sketch,draft}.png.
Run:  python scripts/_designlab_path_backdrops5.py
"""
import base64, os, sys
from openai import OpenAI

SUBJECTS = {
  "histusa": dict(accent="#5b3776", word="muted purple",
    topics=("a vintage Model-T motor car, a jazz saxophone, a Wall Street stock-ticker with a "
            "crashing share-price graph, the Statue of Liberty, art-deco skyscrapers, a 1920s "
            "gramophone, a dust-bowl farmhouse, a Depression-era bread queue")),
  "macbeth": dict(accent="#7d3737", word="muted maroon red",
    topics=("a king's crown, a bloodied dagger, three hooded witch silhouettes, a bubbling cauldron, "
            "a Scottish castle on a crag, a perched raven, an empty throne")),
}

def strict():
    return ("STRICT: vertical portrait. Warm off-white paper (#f7f6f4) fills the ENTIRE image. Place every "
            "drawing ONLY in the far-left and far-right margins; the whole central vertical third MUST stay "
            "completely empty — bare paper, reserved for an overlay. Keep everything pale, faded and "
            "low-contrast. ABSOLUTELY NO text, words, letters, numbers, labels or captions. No frame, no "
            "border, no watermark.")

def style_prompt(style, s):
    a, w, t = s["accent"], s["word"], s["topics"]
    if style == "sketch":
        return (f"VERY ROUGH, loose, UNFINISHED hand-sketch — quick scratchy biro/pencil doodles of {t}, "
                f"drawn fast and imperfectly with wobbly lines and several shapes only half-drawn, sparse and "
                f"gestural, NOT a finished drawing. Thin faint single {w} line ({a}) on warm paper, no shading, "
                f"no fills. " + strict())
    return (f"A rough hand-drawn TECHNICAL field-sketch of {t} — loose, gestural, slightly scratchy biro/pencil "
            f"drawings (imperfect, some half-drawn) OVERLAID with light technical scaffolding: faint thin "
            f"construction guide-lines, a subtle drafting grid, small measurement ticks and a stray compass arc, "
            f"like a rough working notebook mixing sketches with blueprint guides. Single {w} ink ({a}) on warm "
            f"paper, no shading, no fills, hand-drawn but with technical guides. " + strict())


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "design-lab", "assets")
    for skey, s in SUBJECTS.items():
        for style in ("sketch", "draft"):
            out_path = os.path.join(out_dir, f"path-bg-{skey}-{style}.png")
            for model in ("gpt-image-2", "gpt-image-1"):
                try:
                    print(f"[{skey}-{style}] {model}…", flush=True)
                    r = client.images.generate(model=model, prompt=style_prompt(style, s), size="1024x1536", quality="high")
                    with open(out_path, "wb") as f:
                        f.write(base64.b64decode(r.data[0].b64_json))
                    print(f"[{skey}-{style}] saved ({os.path.getsize(out_path)//1024} KB) via {model}", flush=True)
                    break
                except Exception as e:
                    print(f"[{skey}-{style}] {model} failed: {e}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
