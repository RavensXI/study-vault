# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_geometry-L01_maths-ocr.json", encoding="utf-8"))

def check(disp, tag):
    for m in re.finditer(r'<svg viewBox="0 0 (\d+) (\d+)"', disp):
        w, h = int(m.group(1)), int(m.group(2))
    if "<svg" not in disp: return
    w = int(re.search(r'viewBox="0 0 (\d+) (\d+)"', disp).group(1))
    h = int(re.search(r'viewBox="0 0 (\d+) (\d+)"', disp).group(2))
    # gather all x/y coords from text, line, circle, polyline, polygon
    oob = []
    for xm in re.finditer(r'(?:x|x1|x2|cx)="(-?\d+\.?\d*)"', disp):
        v = float(xm.group(1))
        if v < -2 or v > w+2: oob.append(("x", v, w))
    for ym in re.finditer(r'(?:y|y1|y2|cy)="(-?\d+\.?\d*)"', disp):
        v = float(ym.group(1))
        if v < -2 or v > h+2: oob.append(("y", v, h))
    for pm in re.finditer(r'points="([^"]+)"', disp):
        for pair in pm.group(1).split():
            x, y = pair.split(",")
            if float(x) < -2 or float(x) > w+2: oob.append(("px", float(x), w))
            if float(y) < -2 or float(y) > h+2: oob.append(("py", float(y), h))
    if oob:
        print(f"OOB {tag} (vb {w}x{h}):", oob[:6])
    else:
        print(f"ok  {tag} (vb {w}x{h}), len={len(disp)}")

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        check(p["display"], f"{tier}[{i}]")
check(pd["guided"]["opener"]["display"], "opener")
for t in ("bronze","silver","gold"):
    check(pd["guided"]["teach"][t]["display"], f"teach.{t}")
