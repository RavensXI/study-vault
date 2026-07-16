# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_geometry-L04_diagrams.json", encoding="utf-8"))
want = [("silver",4),("silver",6),("gold",0),("gold",1),("gold",4)]
cells=[]
for t,i in want:
    d=pd["problem_bank"][t][i]["display"]
    svg=d[:d.find("</svg>")+6]
    txt=re.sub(r"<svg.*?</svg>","",d)
    cells.append('<div class=c><b>%s[%d]</b><br>%s<div class=t>%s</div></div>'%(t,i,svg,txt))
html=('<!doctype html><meta charset=utf-8><style>body{background:#faf8f5;color:#2d2a26;'
 'font-family:Inter;padding:10px}.c{display:inline-block;vertical-align:top;width:300px;'
 'border:1px solid #ccc;border-radius:8px;padding:8px;margin:5px;background:#fff}'
 '.t{font-size:10px;color:#555}svg{border:1px dashed #eee}</style>'+"".join(cells))
io.open("_gallery2_gL04.html","w",encoding="utf-8").write(html)
print("ok")
