import json,re
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
for tier,i in [("bronze",6),("silver",3)]:
    d=pb[tier][i]["display"]
    svg=re.search(r'<svg.*?</svg>',d,flags=re.S).group(0)
    # print circles, arrows(line with marker), texts
    print(f"\n### {tier}[{i}]")
    for tag in ['circle','text','line','polyline','path','defs','marker']:
        for m in re.finditer(rf'<{tag}[^>]*>(?:[^<]*</'+tag+'>)?',svg):
            frag=m.group(0)
            if tag=='line' and "stroke-opacity='0.10'" in frag: continue
            print("  ",frag[:180])
