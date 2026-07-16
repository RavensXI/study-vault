import json, io
pd=json.load(io.open("lesson_geometry-L01_diagrams.json",encoding="utf-8"))
want=[("silver",6),("gold",1),("gold",3),("gold",4)]
cards=[]
for tier,i in want:
    p=pd["problem_bank"][tier][i]
    cards.append(f'<div class="c"><div class="t">{tier}[{i}]</div><div class="d">{p["display"]}</div></div>')
html='<!doctype html><meta charset=utf-8><style>body{background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif}.c{display:inline-block;width:290px;vertical-align:top;margin:8px;padding:8px;border:1px solid #ccc;border-radius:12px;background:#fff}.t{font-weight:700;font-size:12px;margin-bottom:4px}.figure-caption{display:block;font-size:11px;color:#777;text-align:center;font-style:italic}svg{color:#2d2a26}</style>'+"".join(cards)
io.open("_preview_geomL01b.html","w",encoding="utf-8").write(html)
print("ok")
