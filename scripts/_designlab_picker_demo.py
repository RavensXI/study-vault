"""Picker demo loop for the landing page (Tom, 12 Jul): a looping product
demo assembled from headless state renders — cursor glides between subject
cards, click pulses, crossfades, ending on the exam-boards step.

Self-contained: renders the states itself (serve.py must be running on :8901),
then assembles picker_demo.mp4 (production, ~300KB) + .gif + a QA filmstrip
into ./_demo_out. Re-run whenever the picker design changes.

Run: python scripts/_designlab_picker_demo.py
"""
import os, subprocess, sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://localhost:8901/design-lab/home-study.html?snap&"
STATES = [
    "view=picker&picked=maths,lang,lit,science",
    "view=picker&picked=maths,lang,lit,science,history",
    "view=picker&picked=maths,lang,lit,science,history,geog",
    "view=picker&picked=maths,lang,lit,science,history,geog,french",
    "view=picker&picked=maths,lang,lit,science,history,geog,french,psych",
    "view=boards&picked=maths,lang,lit,science,history,geog,french,psych",
]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_demo_out")
FRAMES_DIR = os.path.join(ROOT, "pickframes")
os.makedirs(FRAMES_DIR, exist_ok=True)
for i, qs in enumerate(STATES):
    out = os.path.join(FRAMES_DIR, f"state{i}.png")
    subprocess.run([CHROME, "--headless=new", "--force-device-scale-factor=1",
        "--hide-scrollbars", "--window-size=1835,1030", "--virtual-time-budget=25000",
        f"--screenshot={out}", BASE + qs], capture_output=True)
    if not os.path.exists(out): sys.exit(f"state {i} failed to render")
    print("rendered state", i)

import os, math, subprocess
from PIL import Image, ImageDraw

S = ROOT
F = os.path.join(S, "pickframes")
CROP = (420, 8, 1420, 1000)          # demo window incl. the Choose-exam-boards CTA
OX, OY = CROP[0], CROP[1]

states = [Image.open(os.path.join(F, f"state{i}.png")).crop(CROP).convert("RGB") for i in range(6)]
W, H = states[0].size

# card centres (canvas coords -> crop coords): the four OPTION picks + the CTA
PT = lambda x, y: (x - OX, y - OY)
CARDS = [PT(570, 499), PT(744, 499), PT(918, 499), PT(1092, 573)]
CTA   = PT(1045, 947)
ENTRY = (W - 60, H - 150)
EXIT  = (W - 40, H - 80)

def ease(t): return t*t*(3-2*t)      # smoothstep

def cursor(draw, x, y):
    pts = [(0,0),(0,17.5),(4.3,13.8),(7.6,21.2),(10.8,19.6),(7.5,12.6),(12.9,12.9)]
    sc = 1.35
    poly = [(x+px*sc, y+py*sc) for px,py in pts]
    sh   = [(px+2, py+2) for px,py in poly]
    draw.polygon(sh, fill=(40,28,12,90))
    draw.polygon(poly, fill=(252,250,246), outline=(35,30,24))

def frame(state, cur=None, pulse=None):
    im = states[state].copy()
    d = ImageDraw.Draw(im, "RGBA")
    if pulse:
        (px, py), t = pulse                  # t 0..1
        r = 8 + t*20
        a = int(150*(1-t))
        d.ellipse([px-r, py-r, px+r, py+r], outline=(196,120,40,a), width=4)
    if cur: cursor(d, *cur)
    return im

frames = []
def hold(state, n, cur=None):
    for _ in range(n): frames.append(frame(state, cur))
def move(state, a, b, n):
    for i in range(1, n+1):
        t = ease(i/n)
        frames.append(frame(state, (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)))
def click(state_before, state_after, at):
    for i in range(3):
        frames.append(frame(state_before, at, ((at[0], at[1]), i/3)))
    for t in (0.45, 0.8):                     # crossfade the new book in
        im = Image.blend(states[state_before], states[state_after], t)
        d = ImageDraw.Draw(im, "RGBA"); cursor(d, *at)
        frames.append(im)

hold(0, 6)                                    # core four already on the shelf
move(0, ENTRY, CARDS[0], 10)
click(0, 1, CARDS[0]); hold(1, 6, CARDS[0])   # + History
move(1, CARDS[0], CARDS[1], 7)
click(1, 2, CARDS[1]); hold(2, 6, CARDS[1])   # + Geography
move(2, CARDS[1], CARDS[2], 7)
click(2, 3, CARDS[2]); hold(3, 6, CARDS[2])   # + French
move(3, CARDS[2], CARDS[3], 8)
click(3, 4, CARDS[3]); hold(4, 8, CARDS[3])   # + Psychology — shelf of eight
move(4, CARDS[3], CTA, 10)
click(4, 5, CTA)                              # Choose exam boards ->
hold(5, 20)                                   # finale: the boards step

FPS = 12
os.makedirs(os.path.join(S, "out"), exist_ok=True)
seq = os.path.join(S, "out")
for i, fr in enumerate(frames):
    fr.save(os.path.join(seq, f"f{i:04d}.png"))
print("frames:", len(frames), "size:", frames[0].size)

# MP4 (the production format for landing-page loops)
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(seq,"f%04d.png"),
    "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-preset","slow",
    os.path.join(S,"picker_demo.mp4")], check=True, capture_output=True)

# GIF (preview / fallback) — palette pass for quality
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(seq,"f%04d.png"),
    "-vf","fps=12,scale=760:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=192[p];[s1][p]paletteuse=dither=sierra2_4a",
    os.path.join(S,"picker_demo.gif")], check=True, capture_output=True)

# QA filmstrip: every 10th frame
strip_frames = frames[::10]
tw = 330; th = int(tw*H/W)
strip = Image.new("RGB", (tw*4+30, th*((len(strip_frames)+3)//4)+20), (60,50,40))
for i, fr in enumerate(strip_frames):
    t = fr.copy(); t.thumbnail((tw, th))
    strip.paste(t, (6+(i%4)*(tw+6), 6+(i//4)*(th+4)))
strip.save(os.path.join(S, "picker_demo_strip.png"))
print("done")
