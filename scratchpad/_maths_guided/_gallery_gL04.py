# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_geometry-L04_diagrams.json", encoding="utf-8"))
cells = []
def add(name, disp):
    svg = disp[:disp.find("</svg>")+6] if "<svg" in disp else ""
    txt = re.sub(r"<svg.*?</svg>", "", disp)
    cells.append('<div class="c"><div class="n">%s</div>%s<div class="t">%s</div></div>' % (name, svg, txt))
add("opener", pd["guided"]["opener"]["display"])
for t in ("bronze","silver","gold"):
    add("teach "+t, pd["guided"]["teach"][t]["display"])
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        if "<svg" in p["display"]:
            add("%s[%d]"%(t,i), p["display"])
html = ('<!doctype html><meta charset=utf-8><style>'
 'body{background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif;padding:12px}'
 '.g{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}'
 '.c{border:1px solid #ddd;border-radius:8px;padding:6px;background:#fff}'
 '.n{font-weight:700;font-size:11px;margin-bottom:2px}.t{font-size:9px;color:#555;margin-top:2px}'
 'svg{display:block}</style><div class=g>'+"".join(cells)+'</div>'
 '<div style="background:#1a1a1a;color:#eee;margin-top:16px;padding:12px" class=g>'+
 "".join(c.replace('background:#fff','background:#222') for c in cells)+'</div>')
io.open("_gallery_gL04.html","w",encoding="utf-8").write(html)
print("wrote _gallery_gL04.html")
