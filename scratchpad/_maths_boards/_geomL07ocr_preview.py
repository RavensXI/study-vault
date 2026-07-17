# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_maths-ocr_geometry-L07.json", encoding="utf-8"))
parts = ['<!doctype html><meta charset="utf-8"><style>body{background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif;padding:16px}'
         '.cell{display:inline-block;width:270px;height:280px;overflow:hidden;vertical-align:top;margin:6px;padding:6px;border:1px solid #ccc;border-radius:12px;background:#fff}'
         '.figure-caption{display:block;font-size:11px;color:#888;font-style:italic;margin-top:4px}h3{margin:2px;font-size:13px}</style>']
def add(title, disp):
    svg = re.search(r'<svg.*?</svg>', disp, re.S)
    svg = svg.group(0) if svg else ''
    parts.append('<div class="cell"><h3>%s</h3>%s</div>' % (title, svg))
add("OPENER", pd["guided"]["opener"]["display"])
for t in ("bronze","silver","gold"):
    add("teach."+t, pd["guided"]["teach"][t]["display"])
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        add("%s[%d] sol=%s"%(t,i,p["solutions"]), p["display"])
io.open("_geomL07ocr_preview.html","w",encoding="utf-8").write("".join(parts))
print("wrote _geomL07ocr_preview.html")
