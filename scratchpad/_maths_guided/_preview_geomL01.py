import json, io
pd=json.load(io.open("lesson_geometry-L01_diagrams.json",encoding="utf-8"))
cards=[]
def card(title, disp):
    return f'<div class="c"><div class="t">{title}</div><div class="d">{disp}</div></div>'
cards.append(card("OPENER", pd["guided"]["opener"]["display"]))
for tier in ("bronze","silver"):
    cards.append(card(f"TEACH {tier}", pd["guided"]["teach"][tier]["display"]))
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if "<svg" in p["display"]:
            cards.append(card(f"{tier}[{i}]", p["display"]))
html='<!doctype html><meta charset=utf-8><style>body{background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif}.c{display:inline-block;width:290px;vertical-align:top;margin:8px;padding:8px;border:1px solid #ccc;border-radius:12px;background:#fff}.t{font-weight:700;font-size:12px;margin-bottom:4px}.figure-caption{display:block;font-size:11px;color:#777;text-align:center;font-style:italic}svg{color:#2d2a26}</style>'+"".join(cards)
io.open("_preview_geomL01.html","w",encoding="utf-8").write(html)
print("wrote", len(cards),"cards")
