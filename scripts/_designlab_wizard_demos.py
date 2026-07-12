"""Wizard demo loops for the landing page (Tom, 12 Jul): three staged product
loops — subjects, boards, topics — plus the full ~26s journey cut, assembled
from headless state renders with an animated cursor, click pulses, crossfades.

Run: python scripts/_designlab_wizard_demos.py   (serve.py on :8901)
Outputs in scripts/_demo_out: wizard_pick / wizard_boards / wizard_topics
(.mp4 + .gif each), wizard_full.mp4, and a QA strip per loop.
"""
import os, subprocess, sys, math
from PIL import Image, ImageDraw

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://localhost:8901/design-lab/home-study.html?snap&"
P8 = "picked=maths,lang,lit,science,history,geog,french,psych"
B5 = "boards=maths:edexcel,lang:aqa,science:aqa,geog:aqa,french:aqa"
B8 = "boards=maths:edexcel,lang:aqa,science:aqa,geog:aqa,french:aqa,lit:aqa,history:aqa,psych:aqa"
T6 = ("tsel=history.0.america-opportunity-inequality,history.1.conflict-tension-east-west,"
      "history.2.britain-health-people,lit.0.macbeth,lit.1.a-christmas-carol,lit.3.power-and-conflict")
T7 = T6 + ",lit.2.an-inspector-calls"
T8 = T7 + ",history.3.elizabethan-england"

STATES = {
    "a0": f"view=picker&picked=maths,lang,lit,science",
    "a1": f"view=picker&picked=maths,lang,lit,science,history",
    "a2": f"view=picker&picked=maths,lang,lit,science,history,geog",
    "a3": f"view=picker&picked=maths,lang,lit,science,history,geog,french",
    "a4": f"view=picker&{P8}",
    "bE": f"view=boards&{P8}",
    "b0": f"view=boards&{P8}&{B5}",
    "b1": f"view=boards&{P8}&{B5},lit:aqa",
    "b2": f"view=boards&{P8}&{B5},lit:aqa,history:aqa",
    "b3": f"view=boards&{P8}&{B8}",
    "c0": f"view=topics&{P8}&{B8}&{T6}",
    "c1": f"view=topics&{P8}&{B8}&{T7}",
    "c2": f"view=topics&{P8}&{B8}&{T8}",
    "sF": f"view=save&{P8}&{B8}&{T8}",
}

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

CROP = (420, 8, 1420, 1148)
OX, OY = CROP[0], CROP[1]
S = {k: Image.open(os.path.join(FD, f"{k}.png")).crop(CROP).convert("RGB") for k in STATES}
W, H = S["a0"].size
PT = lambda x, y: (x - OX, y - OY)

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

def build(seq):
    """seq: list of ops -> frames.  ops: ('hold',st,n,cur) ('move',st,a,b,n) ('click',st1,st2,at)"""
    fr = []
    for op in seq:
        if op[0] == "hold":
            _, st, n, cur = op
            fr += [frame(st, cur) for _ in range(n)]
        elif op[0] == "move":
            _, st, a, b, n = op
            for i in range(1, n+1):
                t = ease(i/n)
                fr.append(frame(st, (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)))
        elif op[0] == "click":
            _, s1, s2, at = op
            for i in range(3): fr.append(frame(s1, at, (at, i/3)))
            for t in (0.45, 0.8):
                im = Image.blend(S[s1], S[s2], t)
                d = ImageDraw.Draw(im, "RGBA"); cursor(d, *at)
                fr.append(im)
        elif op[0] == "fade":
            _, s1, s2, n = op
            fr += [Image.blend(S[s1], S[s2], (i+1)/(n+1)) for i in range(n)]
    return fr

CARDS = [PT(570,499), PT(744,499), PT(918,499), PT(1092,573)]
CTA_A = PT(1045,947)
CHIP_LIT, CHIP_HIS, CHIP_PSY = PT(998,527), PT(998,637), PT(998,802)
NEXT_B = PT(975,911)
CH_INSP, CH_ELIZ, SAVE_C = PT(744,609), PT(753,974), PT(980,1089)
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
    ("move","b3",CHIP_PSY,NEXT_B,7), ("click","b3","c0",NEXT_B), ("hold","c0",14,None),
])
loopC = build([
    ("hold","c0",6,None), ("move","c0",ENTRY,CH_INSP,10),
    ("click","c0","c1",CH_INSP), ("hold","c1",6,CH_INSP),
    ("move","c1",CH_INSP,CH_ELIZ,9), ("click","c1","c2",CH_ELIZ), ("hold","c2",8,CH_ELIZ),
    ("move","c2",CH_ELIZ,SAVE_C,8), ("click","c2","sF",SAVE_C), ("hold","sF",16,None),
])
full = loopA[:-14] + build([("fade","bE","b0",3)]) + loopB[6:] + loopC[6:]

FPS = 12
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
    # QA strip
    sel = frames[::12]
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
print("done ->", ROOT)
