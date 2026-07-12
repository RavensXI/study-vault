"""Wizard demo loops for the landing page (Tom, 12 Jul): three staged product
loops — subjects, boards, topics — plus the full journey cut, assembled from
headless state renders with an animated cursor, click pulses and crossfades.

24fps; every CTA click target is located by pixel-scanning the state render
(no hardcoded button coords). The full cut finishes honestly: four topic
questions at normal pace, a fast-forward montage through the rest, then a
real click on "Save your choices".

Run: python scripts/_designlab_wizard_demos.py   (serve.py on :8901)
Outputs in scripts/_demo_out: wizard_pick / wizard_boards / wizard_topics
(.mp4 + .gif each), wizard_full.mp4, and a QA strip per loop.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://localhost:8901/design-lab/home-study.html?snap&"
P8 = "picked=maths,lang,lit,science,history,geog,french,psych"
B5 = "boards=maths:edexcel,lang:aqa,science:aqa,geog:aqa,french:aqa"
B8 = "boards=maths:edexcel,lang:aqa,science:aqa,geog:aqa,french:aqa,lit:aqa,history:aqa,psych:aqa"

TS1 = "tsel=lit.0.macbeth"
TS2 = TS1 + ",lit.1.a-christmas-carol"
TS3 = TS2 + ",lit.2.an-inspector-calls"
TS4 = TS3 + ",lit.3.power-and-conflict"
TH1 = TS4 + ",history.0.america-opportunity-inequality"
TH2 = TH1 + ",history.1.conflict-tension-east-west"
TH3 = TH2 + ",history.2.britain-health-people"
TH4 = TH3 + ",history.3.elizabethan-england"
TG1 = TH4 + ",geog.0.hot-deserts"
TG2 = TG1 + ",geog.1.coasts~rivers"
TG3 = TG2 + ",geog.2.energy"

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
    "c0":  f"view=topics&{P8}&{B8}&tsel=&tstep=0",
    "c0s": f"view=topics&{P8}&{B8}&{TS1}&tstep=0",
    "c1":  f"view=topics&{P8}&{B8}&{TS1}&tstep=1",
    "c1s": f"view=topics&{P8}&{B8}&{TS2}&tstep=1",
    "c2":  f"view=topics&{P8}&{B8}&{TS2}&tstep=2",
    "c2s": f"view=topics&{P8}&{B8}&{TS3}&tstep=2",
    "c3":  f"view=topics&{P8}&{B8}&{TS3}&tstep=3",
    # fast-forward montage: each remaining question shown answered
    "m3":  f"view=topics&{P8}&{B8}&{TS4}&tstep=3",
    "m4":  f"view=topics&{P8}&{B8}&{TH1}&tstep=4",
    "m5":  f"view=topics&{P8}&{B8}&{TH2}&tstep=5",
    "m6":  f"view=topics&{P8}&{B8}&{TH3}&tstep=6",
    "m7":  f"view=topics&{P8}&{B8}&{TH4}&tstep=7",
    "m8":  f"view=topics&{P8}&{B8}&{TG1}&tstep=8",
    "m9":  f"view=topics&{P8}&{B8}&{TG2}&tstep=9",
    "m10": f"view=topics&{P8}&{B8}&{TG3}&tstep=10",
    "sF":  f"view=save&{P8}&{B8}&{TG3}",
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

def find_cta(key, ymin=500):
    """Locate the enabled (dark) CTA button in a state render."""
    a = np.array(S[key])
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    m = (r<125)&(g<110)&(b<95)&(r>=g)&(g>=b)
    m[:ymin,:] = False
    rows = m.sum(axis=1)
    ys = np.where(rows>80)[0]
    if not len(ys): raise RuntimeError(f"no CTA found in {key}")
    band = m[ys.min():ys.max()+1]
    xs = np.where(band.any(axis=0))[0]
    return (int(xs.mean()), int((ys.min()+ys.max())/2))

NS = 2                      # smoothness scale: op counts were tuned at 12fps
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

def build(seq):
    fr = []
    for op in seq:
        if op[0] == "hold":
            _, st, n, cur = op
            fr += [frame(st, cur) for _ in range(n*NS)]
        elif op[0] == "flash":                       # montage beat — no NS scaling
            _, st, n = op
            fr += [frame(st) for _ in range(n)]
        elif op[0] == "move":
            _, st, a, b, n = op
            for i in range(1, n*NS+1):
                t = ease(i/(n*NS))
                fr.append(frame(st, (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)))
        elif op[0] == "click":
            _, s1, s2, at = op
            for i in range(3*NS): fr.append(frame(s1, at, (at, i/(3*NS))))
            for t in (0.3, 0.55, 0.75, 0.9):
                im = Image.blend(S[s1], S[s2], t)
                d = ImageDraw.Draw(im, "RGBA"); cursor(d, *at)
                fr.append(im)
        elif op[0] == "fade":
            _, s1, s2, n = op
            fr += [Image.blend(S[s1], S[s2], (i+1)/(n*NS+1)) for i in range(n*NS)]
    return fr

CARDS = [PT(570,499), PT(744,499), PT(918,499), PT(1092,573)]
CHIP_LIT, CHIP_HIS, CHIP_PSY = PT(998,527), PT(998,637), PT(998,802)
CHIP_MAC, CHIP_ACC, CHIP_AIC = PT(572,532), PT(653,533), PT(638,532)
CTA_A  = find_cta("a4", 880)
NEXT_B = find_cta("b3", 850)
N0, N1, N2 = find_cta("c0s"), find_cta("c1s"), find_cta("c2s")
SAVE_M = find_cta("m10", 555)
ENTRY = (W-60, H-260)
ASIDE = (W-50, H-180)

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
montage = [("flash",k,4) for k in ("m3","m4","m5","m6","m7","m8","m9")] + [("flash","m10",7)]
loopC = build([
    ("hold","c0",6,None), ("move","c0",ENTRY,CHIP_MAC,10),
    ("click","c0","c0s",CHIP_MAC), ("hold","c0s",5,CHIP_MAC),
    ("move","c0s",CHIP_MAC,N0,6), ("click","c0s","c1",N0), ("hold","c1",4,N0),
    ("move","c1",N0,CHIP_ACC,6), ("click","c1","c1s",CHIP_ACC), ("hold","c1s",4,CHIP_ACC),
    ("move","c1s",CHIP_ACC,N1,6), ("click","c1s","c2",N1), ("hold","c2",4,N1),
    ("move","c2",N1,CHIP_AIC,6), ("click","c2","c2s",CHIP_AIC), ("hold","c2s",4,CHIP_AIC),
    ("move","c2s",CHIP_AIC,N2,6), ("click","c2s","c3",N2), ("hold","c3",5,None),
    ("move","c3",N2,ASIDE,5),                          # cursor steps aside…
    ] + montage + [                                    # …the rest answer themselves
    ("move","m10",ASIDE,SAVE_M,7), ("click","m10","sF",SAVE_M),
    ("hold","sF",16,None),
])
full = loopA[:-(14*NS)] + build([("fade","bE","b0",3)]) + loopB[6*NS:] + loopC[6*NS:]

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
print("done ->", ROOT)
