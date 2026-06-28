"""Postcard concept: 2-3 DELIBERATE, clearly-separated painterly panels (not blended).
Each is its own self-contained vignette of a different slice of the unit, framed like a
postcard and laid on warm paper with clear gaps. Output: design-lab/assets/_postcards.png
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_aligned_ladder import motifs_for
from _designlab_strip import split_subjects
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
SKEY, SLUG, NSEG = "science-aqa", "biology-paper-1", 3

STYLE = ("Soft PAINTERLY GOUACHE illustration in a warm muted sage-green and cream palette, gentle brushwork and "
         "light, the subjects nestled together into one small self-contained painted scene that fills the frame. "
         "Distinct recognisable objects — NOT joined by veins/tubes, NO text, letters or numbers. Warm off-white paper.")

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(prompt, out):
    cfg = types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="3:2"))
    for c in (cfg, types.GenerateContentConfig(response_modalities=["IMAGE"])):
        try:
            r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt], config=c)
            d = extract(r)
            if d:
                open(out, "wb").write(d); return out
        except Exception as e:
            print("  err", str(e)[:120], flush=True)
    return None

def postcards(imgs, H=300, pad=22, gap=30, mat=12):
    cardH = H - 2 * pad
    framed = []
    for im in imgs:
        iw = round(im.width * (cardH - 2 * mat) / im.height)
        inner = im.resize((iw, cardH - 2 * mat))
        cw = iw + 2 * mat
        card = Image.new("RGB", (cw, cardH), (250, 247, 240))      # cream mat
        card.paste(inner, (mat, mat))
        ImageDraw.Draw(card).rectangle([0, 0, cw - 1, cardH - 1], outline=(168, 158, 142), width=1)
        framed.append(card)
    totalW = sum(c.width for c in framed) + gap * (len(framed) - 1) + 2 * pad
    canvas = Image.new("RGB", (totalW, H), (244, 240, 232))        # warm paper
    # soft drop shadows
    shadow = Image.new("RGBA", (totalW, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x = pad
    for c in framed:
        sd.rectangle([x + 3, pad + 6, x + c.width + 3, pad + c.height + 6], fill=(40, 34, 26, 70))
        x += c.width + gap
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(7))).convert("RGB")
    x = pad
    for c in framed:
        canvas.paste(c, (x, pad)); x += c.width + gap
    return canvas

subs = split_subjects(motifs_for(SKEY, SLUG))
groups = [subs[i::NSEG] for i in range(NSEG)]
imgs = []
for gi, grp in enumerate(groups):
    subj = ", ".join(grp)
    p = gen(f"A small self-contained painted scene of these GCSE Biology subjects: {subj}. {STYLE}", os.path.join(ASSETS, f"_pc-{gi}.png"))
    if p:
        imgs.append(Image.open(p).convert("RGB")); print(f"panel {gi}: {grp}", flush=True)
out = os.path.join(ASSETS, "_postcards.png")
postcards(imgs).save(out)
print("saved", Image.open(out).size, flush=True)
