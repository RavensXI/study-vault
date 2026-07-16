import json
pd=json.load(open("lesson_geometry-L06.json",encoding="utf-8"))
d=pd["problem_bank"]["silver"][0]["display"]
svg=d[:d.index("</svg>")+6]
svg=svg.replace('currentColor','#222')
open("_L06_check.svg","w",encoding="utf-8").write(svg)
try:
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode(),write_to="_L06_check.png",output_width=480)
    print("PNG written")
except Exception as e:
    print("no cairosvg:",e)
