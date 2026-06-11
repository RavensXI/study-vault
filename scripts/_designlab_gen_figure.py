"""Design-lab one-off: generate a single lesson diagram with gpt-image-2.

Two-step pattern (per memory/gpt_image_2_evaluation.md): the prompt below is the
"Claude wrote the prompt" half; this script is just the image call. Saves a PNG
into design-lab/assets/ so the local serve.py (root = worktree) can serve it.

Run:  python scripts/_designlab_gen_figure.py
"""
import base64
import os
import sys
from openai import OpenAI

ACCENT = "#7d4f41"  # history umber — matches the Reader skin's history accent

PROMPT = f"""A clean, modern, flat-vector educational science diagram illustrating
Louis Pasteur's swan-neck flask experiment that disproved spontaneous generation.

Two labelled glass flasks side by side on an off-white background, with a clear
title at the top: "Pasteur's Swan-Neck Flask Experiment".

LEFT flask — labelled "Neck intact": a round-bottomed flask with a long, intact
S-shaped 'swan neck' that curves down then up. Clear broth inside. Small dust
particles and microbes (tiny dots) shown settling and trapped in the low bend of
the curved neck, unable to reach the broth. A caption beneath: "Broth boiled, then
left — stays clear. Microbes trapped in the bend."

RIGHT flask — labelled "Neck broken": the same flask but with the swan neck snapped
off short and open to the air. Airborne dust and microbes (tiny dots) drifting down
into the broth. The broth shown cloudy/murky. A caption beneath: "Neck snapped off —
broth turns cloudy as microbes grow."

A small curved arrow or "vs" between the two flasks to show the comparison.

Style: flat vector illustration, restrained palette of warm umber ({ACCENT}) for the
title, labels and accents, with soft warm greys and off-white; broth a pale tone,
cloudy broth a muted murky tone. Clean sans-serif labels, generous spacing, accurate
glassware shapes, high legibility, education-textbook quality. No photorealism, no
3D, no clutter, no watermark. Landscape composition."""


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "design-lab", "assets")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "pasteur-swan-neck.png")

    for model in ("gpt-image-2", "gpt-image-1"):
        try:
            print(f"Generating with {model} (1536x1024, high)…")
            r = client.images.generate(
                model=model,
                prompt=PROMPT,
                size="1536x1024",
                quality="high",
            )
            b64 = r.data[0].b64_json
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(b64))
            print(f"Saved {out_path} ({os.path.getsize(out_path)//1024} KB) via {model}")
            return
        except Exception as e:
            print(f"  {model} failed: {e}")
    sys.exit("All models failed")


if __name__ == "__main__":
    main()
