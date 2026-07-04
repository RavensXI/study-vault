"""Desk4 flashcard scatter plate — a loose pile of index cards, drawn in the
scene's line-and-wash style. The scatter is only a DOOR to flashcard mode
(one click target); the clean top card gets a live handwritten question
homography-mapped onto it in dash-desk4.html (.fcq matrix3d).

Chosen plate: desk4-cards-a-cut.png (2210x1489), b = alternate.
"""
import os, io, time
from google.genai import types
from PIL import Image
from _designlab_desk4_book import client, IMG_MODEL, extract, cut, OUT

PROMPT = (
    "In exactly the style of the attached reference image (hand-drawn pen-and-ink with soft "
    "watercolour wash, warm muted colours), draw ONE group of objects on a plain warm cream "
    "paper background: a loose scatter of seven cream index cards lying on a desk, seen from a "
    "seated three-quarter view slightly above. The cards overlap casually at different small "
    "angles, like someone has been shuffling through them; a few faint grey-blue ruled lines on "
    "each card; two or three of the cards carry loose, completely ILLEGIBLE pencil squiggles "
    "that merely suggest handwriting — absolutely NOT real letters, numbers or words. ONE clean "
    "card lies on top of the pile, blank, tilted a few degrees. Thin ink outlines, soft "
    "watercolour shadows beneath each card. The scatter fills most of the frame. "
    "ABSOLUTELY NO real text, letters or numbers anywhere."
)

if __name__ == "__main__":
    scene = open(os.path.join(OUT, "desk4-scene-a.png"), "rb").read()
    for tag in ("a", "b"):
        raw = os.path.join(OUT, f"desk4-cards-{tag}.png")
        img = None
        if not os.path.exists(raw):
            for attempt in range(4):
                try:
                    r = client.models.generate_content(model=IMG_MODEL,
                        contents=[PROMPT, types.Part.from_bytes(data=scene, mime_type="image/png")],
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                            image_config=types.ImageConfig(aspect_ratio="4:3", image_size="2K")))
                    d = extract(r)
                    if d:
                        img = Image.open(io.BytesIO(d)).convert("RGB"); break
                except Exception as e:
                    msg = str(e)
                    if any(k in msg for k in ("502", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                        time.sleep(6 * (attempt + 1)); continue
                    print("  err:", msg[:110], flush=True)
            if img is None:
                print("FAIL", tag, flush=True); continue
            img.save(raw)
        w, h = cut(raw, os.path.join(OUT, f"desk4-cards-{tag}-cut.png"))
        print(f"ok   {tag}  cut {w}x{h}", flush=True)
    print("done")
