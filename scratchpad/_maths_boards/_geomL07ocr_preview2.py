# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_maths-ocr_geometry-L07.json", encoding="utf-8"))
parts = ['<!doctype html><meta charset="utf-8"><style>body{background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif;padding:16px}'
         '.cell{display:inline-block;width:270px;height:300px;overflow:hidden;vertical-align:top;margin:6px;padding:6px;border:1px solid #ccc;border-radius:12px;background:#fff}'
         'h3{margin:2px;font-size:13px}</style>']
def svgof(disp):
    m = re.search(r'<svg.*?</svg>', disp, re.S)
    return m.group(0) if m else ''
def add(title, disp):
    parts.append('<div class="cell"><h3>%s</h3>%s</div>' % (title, svgof(disp)))
want = [("silver",3),("silver",5),("silver",6),("gold",0),("gold",1),("gold",2),("gold",3),("gold",4)]
for t,i in want:
    p = pd["problem_bank"][t][i]
    add("%s[%d] sol=%s"%(t,i,p["solutions"]), p["display"])
io.open("_geomL07ocr_preview2.html","w",encoding="utf-8").write("".join(parts))
print("ok")
