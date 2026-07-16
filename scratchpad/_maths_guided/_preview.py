import json,re
pd=json.load(open("lesson_algebra-L10_diagrams.json",encoding="utf-8"))
svgs=[re.search(r'(<svg.*?</svg>)',g["display"]).group(1) for g in pd["problem_bank"]["gold"][:4]]
html='<div style="color:#2d2a26;background:#faf8f5;padding:16px;display:flex;gap:12px;flex-wrap:wrap">'+ "".join('<div style="border:1px solid #ccc">%s</div>'%s for s in svgs)+'</div>'
html+='<div style="color:#eee;background:#1a1a1a;padding:16px;display:flex;gap:12px;flex-wrap:wrap">'+ "".join('<div style="border:1px solid #444">%s</div>'%s for s in svgs)+'</div>'
open("_preview.html","w",encoding="utf-8").write("<!doctype html><meta charset=utf-8>"+html)
print("wrote _preview.html")
