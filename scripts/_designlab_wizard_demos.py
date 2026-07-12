# -*- coding: utf-8 -*-
"""Wizard demo loops for the landing page: three staged loops (subjects,
boards, topics teaser) + wizard_full, the COMPLETE journey — every subject
pick, every board, all eleven topic questions clicked for real, account card.

Coordinates are never guessed: the page's ?probe hook reports the centre of
every clickable control (read via --dump-dom), and a click-QA sheet is
exported so every click can be verified against its control.

Run: python scripts/_designlab_wizard_demos.py   (serve.py on :8901)
Outputs in scripts/_demo_out.
"""
import os, subprocess, sys, json, re, html
from PIL import Image, ImageDraw

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://localhost:8901/design-lab/home-study.html?snap&"
P8 = "picked=maths,lang,lit,science,history,geog,french,psych"
B5 = "boards=maths:edexcel,lang:aqa,science:aqa,geog:aqa,french:aqa"
B8 = "boards=maths:edexcel,lang:aqa,science:aqa,geog:aqa,french:aqa,lit:aqa,history:aqa,psych:aqa"

# the eleven topic answers for this subject mix, in question order
ANSWERS = [
    "lit.0.macbeth", "lit.1.a-christmas-carol", "lit.2.an-inspector-calls",
    "lit.3.power-and-conflict",
    "history.0.america-opportunity-inequality", "history.1.conflict-tension-east-west",
    "history.2.britain-health-people", "history.3.elizabethan-england",
    "geog.0.hot-deserts", "geog.1.coasts~rivers", "geog.2.energy",
]
# the chip label(s) the cursor clicks on each question (exact textContent)
CLICKS = [
    ["Macbeth"], ["A Christmas Carol"], ["An Inspector Calls"], ["Power & Conflict"],
    ["America, 1920–1973"], ["East and West, 1945–72"],
    ["Health and the People"], ["Elizabethan England"],
    ["Hot Deserts"], ["Coastal Landscapes", "River Landscapes"], ["Energy"],
]
NQ = len(ANSWERS)
def tsel(k): return "tsel=" + ",".join(ANSWERS[:k])

STATES = {
    "a0": "view=picker&picked=maths,lang,lit,science",
    "a1": "view=picker&picked=maths,lang,lit,science,history",
    "a2": "view=picker&picked=maths,lang,lit,science,history,geog",
    "a3": "view=picker&picked=maths,lang,lit,science,history,geog,french",
    "a4": f"view=picker&{P8}",
    "bE": f"view=boards&{P8}",
    "b0": f"view=boards&{P8}&{B5}",
    "b1": f"view=boards&{P8}&{B5},lit:aqa",
    "b2": f"view=boards&{P8}&{B5},lit:aqa,history:aqa",
    "b3": f"view=boards&{P8}&{B8}",
    "dS": f"view=dash&{P8}&{B8}&{tsel(NQ)}",
}
for k in range(NQ):
    STATES[f"q{k}"]  = f"view=topics&{P8}&{B8}&{tsel(k)}&tstep={k}"      # blank
    STATES[f"q{k}s"] = f"view=topics&{P8}&{B8}&{tsel(k+1)}&tstep={k}"    # answered
STATES["q9a"] = f"view=topics&{P8}&{B8}&{tsel(9)},geog.1.coasts&tstep=9" # 1 of 2 picked

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_demo_out")
FD = os.path.join(ROOT, "wizframes")
os.makedirs(FD, exist_ok=True)

for key, qs in STATES.items():
    out = os.path.join(FD, f"{key}.png")
    if os.path.exists(out): continue
    subprocess.run([CHROME, "--headless=new", "--force-device-scale-factor=1",
        "--hide-scrollbars", "--window-size=1835,1250", "--virtual-time-budget=25000",
        f"--screenshot={out}", BASE + qs], capture_output=True)
    if not os.path.exists(out): sys.exit(f"state {key} failed")
    print("rendered", key)

PROBES = {}
def probe(state_key):
    """Ask the page itself where its controls are (viewport-centre coords)."""
    if state_key in PROBES: return PROBES[state_key]
    for attempt in range(4):
        r = subprocess.run([CHROME, "--headless=new", "--force-device-scale-factor=1",
            "--hide-scrollbars", "--window-size=1835,1250", "--virtual-time-budget=25000",
            "--dump-dom", BASE + STATES[state_key] + "&probe"],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r'<pre id="proberects">(.*?)</pre>', r.stdout, re.S)
        if m:
            PROBES[state_key] = json.loads(html.unescape(m.group(1)))
            print("probed", state_key)
            return PROBES[state_key]
        print(f"probe retry {attempt+1} for {state_key} (dom {len(r.stdout)} chars)")
    sys.exit(f"probe failed for {state_key}")

CROP = (420, 8, 1420, 1148)
OX, OY = CROP[0], CROP[1]
S = {k: Image.open(os.path.join(FD, f"{k}.png")).crop(CROP).convert("RGB") for k in STATES}
W, H = S["a0"].size
PT = lambda p: (p[0] - OX, p[1] - OY)

NS = 2
FPS = 24

def ease(t): return t*t*(3-2*t)
def cursor(d, x, y):
    pts = [(0,0),(0,17.5),(4.3,13.8),(7.6,21.2),(10.8,19.6),(7.5,12.6),(12.9,12.9)]
    poly = [(x+px*1.35, y+py*1.35) for px, py in pts]
    d.polygon([(px+2, py+2) for px, py in poly], fill=(40,28,12,90))
    d.polygon(poly, fill=(252,250,246), outline=(35,30,24))
def frame(st, cur=None, pulse=None):
    im = S[st].copy(); d = ImageDraw.Draw(im, "RGBA")
    if pulse:
        (px, py), t = pulse; r = 8 + t*20; a = int(150*(1-t))
        d.ellipse([px-r, py-r, px+r, py+r], outline=(196,120,40,a), width=4)
    if cur: cursor(d, *cur)
    return im

CLICK_LOG = []   # (state, at) for the QA sheet
def build(seq):
    fr = []
    for op in seq:
        if op[0] == "hold":
            _, st, n, cur = op
            fr += [frame(st, cur) for _ in range(n*NS)]
        elif op[0] == "move":
            _, st, a, b, n = op
            for i in range(1, n*NS+1):
                t = ease(i/(n*NS))
                fr.append(frame(st, (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)))
        elif op[0] == "click":
            _, s1, s2, at = op
            CLICK_LOG.append((s1, at))
            for i in range(3*NS): fr.append(frame(s1, at, (at, i/(3*NS))))
            for t in (0.3, 0.55, 0.75, 0.9):
                im = Image.blend(S[s1], S[s2], t)
                d = ImageDraw.Draw(im, "RGBA"); cursor(d, *at)
                fr.append(im)
        elif op[0] == "fade":
            _, s1, s2, n = op
            fr += [Image.blend(S[s1], S[s2], (i+1)/(n*NS+1)) for i in range(n*NS)]
    return fr

# ---- probe-driven coordinates ----
PA0, PA4 = probe("a0"), probe("a4")
PB0, PB3 = probe("b0"), probe("b3")
CARDS = [PT(PA0["card_history"]), PT(PA0["card_geog"]), PT(PA0["card_french"]), PT(PA0["card_psych"])]
CTA_A = PT(PA4["pnext"])
CHIP_LIT, CHIP_HIS, CHIP_PSY = PT(PB0["bchip_2_AQA"]), PT(PB0["bchip_4_AQA"]), PT(PB0["bchip_7_AQA"])
NEXT_B = PT(PB3["bnext"])
PQ = [probe(f"q{k}") for k in range(NQ)]
ENTRY = (W-60, H-260)

loopA = build([
    ("hold","a0",6,None), ("move","a0",ENTRY,CARDS[0],10),
    ("click","a0","a1",CARDS[0]), ("hold","a1",5,CARDS[0]),
    ("move","a1",CARDS[0],CARDS[1],7), ("click","a1","a2",CARDS[1]), ("hold","a2",5,CARDS[1]),
    ("move","a2",CARDS[1],CARDS[2],7), ("click","a2","a3",CARDS[2]), ("hold","a3",5,CARDS[2]),
    ("move","a3",CARDS[2],CARDS[3],8), ("click","a3","a4",CARDS[3]), ("hold","a4",7,CARDS[3]),
    ("move","a4",CARDS[3],CTA_A,10), ("click","a4","bE",CTA_A), ("hold","bE",14,None),
])
loopB = build([
    ("hold","b0",6,None), ("move","b0",ENTRY,CHIP_LIT,10),
    ("click","b0","b1",CHIP_LIT), ("hold","b1",5,CHIP_LIT),
    ("move","b1",CHIP_LIT,CHIP_HIS,6), ("click","b1","b2",CHIP_HIS), ("hold","b2",5,CHIP_HIS),
    ("move","b2",CHIP_HIS,CHIP_PSY,7), ("click","b2","b3",CHIP_PSY), ("hold","b3",8,CHIP_PSY),
    ("move","b3",CHIP_PSY,NEXT_B,7), ("click","b3","q0",NEXT_B), ("hold","q0",14,None),
])

def topic_ops(k, prev_at):
    """One question, fully played: click its chip(s), then click Next/Save."""
    ops = []
    labels = CLICKS[k]
    nxt = PT(PQ[k]["tnext"])
    blank, sel = f"q{k}", f"q{k}s"
    if len(labels) == 1:
        at = PT(PQ[k]["chip_" + labels[0]])
        ops += [("move",blank,prev_at,at,6), ("click",blank,sel,at), ("hold",sel,3,at)]
        last = at
    else:                                      # the pick-2 question
        at1, at2 = PT(PQ[k]["chip_"+labels[0]]), PT(PQ[k]["chip_"+labels[1]])
        ops += [("move",blank,prev_at,at1,6), ("click",blank,"q9a",at1), ("hold","q9a",3,at1),
                ("move","q9a",at1,at2,4), ("click","q9a",sel,at2), ("hold",sel,3,at2)]
        last = at2
    target = "dS" if k == NQ-1 else f"q{k+1}"
    ops += [("move",sel,last,nxt,5), ("click",sel,target,nxt), ("hold",target,3 if k<NQ-1 else 0,nxt if k<NQ-1 else None)]
    return ops, nxt

topic_seq = [("hold","q0",5,None)]
prev = ENTRY
for k in range(NQ):
    ops, prev = topic_ops(k, prev)
    topic_seq += ops
topic_seq += [("hold","dS",22,None)]
topicsFull = build(topic_seq)

# the short landing teaser: first three questions, ends resting on Q4
teaser_seq = [("hold","q0",6,None)]
prev = ENTRY
for k in range(3):
    ops, prev = topic_ops(k, prev)
    teaser_seq += ops
teaser_seq += [("hold","q3",12,None)]
loopC = build(teaser_seq)

full = loopA[:-(14*NS)] + build([("fade","bE","b0",3)]) + loopB[6*NS:] + topicsFull[5*NS:]

def export(frames, name, gif=True):
    seq = os.path.join(ROOT, "_seq"); os.makedirs(seq, exist_ok=True)
    for f in os.listdir(seq): os.remove(os.path.join(seq, f))
    for i, fr in enumerate(frames): fr.save(os.path.join(seq, f"f{i:04d}.png"))
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(seq,"f%04d.png"),
        "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-preset","slow",
        os.path.join(ROOT,f"{name}.mp4")], check=True, capture_output=True)
    if gif:
        subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(seq,"f%04d.png"),
            "-vf","fps=12,scale=700:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=192[p];[s1][p]paletteuse=dither=sierra2_4a",
            os.path.join(ROOT,f"{name}.gif")], check=True, capture_output=True)
    sel = frames[::24]
    tw = 300; th = int(tw*H/W)
    strip = Image.new("RGB",(tw*4+30, (th+4)*((len(sel)+3)//4)+16),(60,50,40))
    for i, fr in enumerate(sel):
        t = fr.copy(); t.thumbnail((tw,th))
        strip.paste(t,(6+(i%4)*(tw+6), 6+(i//4)*(th+4)))
    strip.save(os.path.join(ROOT,f"{name}_strip.png"))
    print(name, len(frames), "frames,", round(len(frames)/FPS,1), "s")

export(loopA, "wizard_pick")
export(loopB, "wizard_boards")
export(loopC, "wizard_topics")
export(full, "wizard_full", gif=False)

# click-QA sheet: every click, zoomed on its target, pulse visible
tiles = []
for st, at in CLICK_LOG:
    im = frame(st, at, (at, 0.4))
    x, y = int(at[0]), int(at[1])
    tiles.append(im.crop((max(x-140,0), max(y-80,0), min(x+140,W), min(y+80,H))))
cols = 6
rows = (len(tiles)+cols-1)//cols
sheet = Image.new("RGB", (284*cols+12, 164*rows+12), (60,50,40))
for i, t in enumerate(tiles):
    sheet.paste(t, (6+(i%cols)*284, 6+(i//cols)*164))
sheet.save(os.path.join(ROOT, "click_qa_sheet.png"))
print("click QA sheet:", len(tiles), "clicks")
print("done ->", ROOT)
