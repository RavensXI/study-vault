import json
pd=json.load(open("lesson_geometry-L06.json",encoding="utf-8"))
prob=pd["problem_bank"]["silver"][0]
d=prob["display"]

DEG="°"
# Old 75-degree arc + text placed at P2 (bottom-right, actually 65 deg vertex)
old_arc='<path d="M143.3 141.0 A16 16 0 0 1 152.5 126.5" fill="none" stroke="currentColor" stroke-width="1.3"/>'
old_txt='<text x="138.2" y="127.6" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle">75'+DEG+'</text>'

# New 75-degree arc + text at P1 (bottom-left, the real 75 deg vertex)
new_arc='<path d="M96.7 141.0 A16 16 0 0 0 84.9 125.6" fill="none" stroke="currentColor" stroke-width="1.3"/>'
new_txt='<text x="102.5" y="126.5" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle">75'+DEG+'</text>'

assert old_arc in d, "old arc not found"
assert old_txt in d, "old text not found"
d2=d.replace(old_arc,new_arc).replace(old_txt,new_txt)
assert d2!=d and new_arc in d2 and new_txt in d2
assert "143.3 141.0" not in d2 and "x=\"138.2\"" not in d2
prob["display"]=d2
json.dump(pd, open("lesson_geometry-L06.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("PATCHED display:")
print(d2)
