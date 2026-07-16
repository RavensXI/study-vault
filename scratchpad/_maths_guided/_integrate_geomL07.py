# -*- coding: utf-8 -*-
import json, io, importlib.util, sys

spec = importlib.util.spec_from_file_location("b", "_build_geomL07_fix.py")
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

gd, aC, aD = b.build_gold1()
sd, aO, aC2 = b.build_silver5()
gold_svg = gd.split("</svg>")[0] + "</svg>"
silver_svg = sd.split("</svg>")[0] + "</svg>"

pd = json.load(io.open("_geomL07_LIVE_NOW.json", encoding="utf-8"))

def splice(disp, new_svg):
    tail = disp.split("</svg>", 1)[1]      # preserve caption + question text verbatim
    return new_svg + tail

g = pd["problem_bank"]["gold"][1]
s = pd["problem_bank"]["silver"][5]
old_g, old_s = g["display"], s["display"]
g["display"] = splice(old_g, gold_svg)
s["display"] = splice(old_s, silver_svg)

# sanity: only the SVG changed, question text tail identical
assert old_g.split("</svg>",1)[1] == g["display"].split("</svg>",1)[1], "gold tail changed!"
assert old_s.split("</svg>",1)[1] == s["display"].split("</svg>",1)[1], "silver tail changed!"
# solutions/guided_steps untouched
assert g["solutions"] == [152] and s["solutions"] == [125]

json.dump(pd, io.open("lesson_geometry-L07_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("integrated. gold C=%.1f D=%.1f | silver O=%.1f C=%.1f" % (aC,aD,aO,aC2))
print("gold aria/label swapped, tails preserved verbatim")
