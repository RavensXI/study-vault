"""EXPERIMENT (Tom's idea): give the model a guide image that already has the
trail, numbered stops and lesson titles drawn on it, so it places each motif in
the empty space AROUND them instead of underneath. One 21:9 tile, 5 lessons.

Outputs:
  design-lab/assets/_guide-bio-p1.png      the layout guide we feed in
  design-lab/assets/_guided-bio-p1.png      Gemini's illustrated result
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

W, H = 1584, 672
PAPER = (244, 240, 232)
GREEN = (104, 142, 116)
INK = (60, 58, 54)
TITLES = ["Cell Structure & Microscopy", "Cell Division & Transport",
          "Organisation & the Digestive System", "The Heart, Blood & Circulatory Disease",
          "Health & Non-Communicable Diseases"]
font_t = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
font_n = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def build_guide():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    n = len(TITLES)
    padL = 150
    step = (W - 2 * padL) / (n - 1)
    midY = H / 2
    amp = 42
    pts = [(padL + j * step, midY + math.sin(j * 0.9 + 0.3) * amp) for j in range(n)]
    # the trail (smooth-ish polyline)
    d.line(pts, fill=GREEN, width=7, joint="curve")
    # stops + titles
    for j, (x, y) in enumerate(pts):
        r = 30
        d.ellipse([x - r, y - r, x + r, y + r], fill=GREEN, outline=(255, 255, 255), width=3)
        nt = str(j + 1)
        tw = d.textlength(nt, font=font_n)
        d.text((x - tw / 2, y - 18), nt, fill=(255, 255, 255), font=font_n)
        # title above (even) / below (odd), wrapped, centred
        lines = wrap(d, TITLES[j], font_t, 230)
        above = (j % 2 == 0)
        ty = (y - r - 14 - len(lines) * 30) if above else (y + r + 14)
        for li, ln in enumerate(lines):
            lw = d.textlength(ln, font=font_t)
            d.text((x - lw / 2, ty + li * 30), ln, fill=INK, font=font_t)
    img.save(os.path.join(ASSETS, "_guide-bio-p1.png"))
    return img

def extract(resp):
    for c in (resp.candidates or []):
        for p in (c.content.parts or []):
            dd = getattr(p, "inline_data", None)
            if dd and getattr(dd, "data", None):
                return dd.data
    return None

def illustrate(guide):
    prompt = (
        "This is a learning-path banner for GCSE Biology. It ALREADY has a green winding trail, five numbered "
        "circular stops, and a lesson title beside each stop. Your job is to ILLUSTRATE it: for each numbered "
        "stop, draw ONE detailed, relevant biology motif (matching that stop's title) in the empty paper space on "
        "the OPPOSITE side of the trail from its title, centred on that stop's column. "
        "CRITICAL RULES: keep the green trail, the five numbered circles and ALL the title text EXACTLY as they "
        "are and fully legible — do not cover, move or redraw them. Only add illustrations in the blank paper. "
        "Leave a clear gap around every circle and every title. Warm off-white paper, soft natural light, gentle "
        "green tones. Do not add any extra text, words, numbers or labels of your own."
    )
    cfgs = [types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="21:9")),
            types.GenerateContentConfig(response_modalities=["IMAGE"])]
    for cfg in cfgs:
        try:
            r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt, guide], config=cfg)
            data = extract(r)
            if data:
                out = os.path.join(ASSETS, "_guided-bio-p1.png")
                open(out, "wb").write(data)
                print("saved", out, Image.open(out).size, flush=True)
                return
        except Exception as e:
            print("err", str(e)[:140], flush=True)
    print("failed")

def illustrate_blank(guide):
    prompt = (
        "The green winding trail, the five numbered circles and the lesson titles in this image are ONLY a layout "
        "guide telling you WHERE the user interface will go. Illustrate a GCSE Biology banner: near each numbered "
        "stop, draw ONE detailed biology motif in the blank paper on the OPPOSITE side of the trail from that "
        "stop's title. "
        "CRITICAL: in your final image do NOT draw the green trail, the circles, or ANY text/numbers — render all "
        "of those areas, and the whole central horizontal lane, as clean EMPTY warm off-white paper. Keep a clear "
        "blank gap where each title sits. Only the biology illustrations should appear, arranged top and bottom. "
        "Soft natural light, gentle green tones."
    )
    cfgs = [types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="21:9")),
            types.GenerateContentConfig(response_modalities=["IMAGE"])]
    for cfg in cfgs:
        try:
            r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt, guide], config=cfg)
            data = extract(r)
            if data:
                out = os.path.join(ASSETS, "_guided-bio-p1-B.png")
                open(out, "wb").write(data); print("saved", out, flush=True); return
        except Exception as e:
            print("errB", str(e)[:140], flush=True)
    print("failed B")

g = build_guide()
print("guide built", flush=True)
illustrate(g)
illustrate_blank(g)
