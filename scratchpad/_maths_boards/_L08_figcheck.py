# -*- coding: utf-8 -*-
import json, re
pd = json.load(open("lesson_maths-eduqas_geometry-L08_diagrams.json", encoding="utf-8"))
pb = pd["problem_bank"]
targets = [("bronze",6),("silver",0),("silver",1),("silver",2),("silver",3),
           ("silver",5),("gold",0),("gold",1)]
html = ["<!doctype html><meta charset=utf-8><style>body{background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif}div{display:inline-block;border:1px solid #ccc;margin:8px;padding:8px;vertical-align:top;width:250px}.figure-caption{font-size:11px;font-style:italic;opacity:.7}</style>"]
for t,i in targets:
    disp = pb[t][i]["display"]
    # bounds check
    for m in re.finditer(r"<svg viewBox='0 0 (\d+) (\d+)'", disp):
        W,H = int(m.group(1)), int(m.group(2))
    svg = disp[:disp.find("</svg>")+6]
    nums = [float(x) for x in re.findall(r"(?:x|y|cx|cy|x1|y1|x2|y2)='(-?\d+\.?\d*)'", svg)]
    print(f"{t}[{i}] viewBox {W}x{H}  coord range x/y approx max={max(nums):.0f} min={min(nums):.0f}")
    html.append(f"<div><b>{t}[{i}]</b><br>{disp}</div>")
open("_L08_figcheck.html","w",encoding="utf-8").write("".join(html))
print("wrote _L08_figcheck.html")
