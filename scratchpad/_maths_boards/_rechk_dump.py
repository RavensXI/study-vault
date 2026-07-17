import json,re
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
def clean(s):
    return re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
for tier in ["bronze","silver","gold"]:
    print(f"\n########## {tier.upper()} ##########")
    for i,p in enumerate(pb[tier]):
        print(f"\n----- {tier}[{i}] -----")
        print("DISPLAY:",clean(p.get('display','')))
        print("OPTIONS:",p.get('options'))
        print("SOLUTIONS(idx):",p.get('solutions'))
        print("HINT:",p.get('hint'))
        mis=p.get('misconceptions',[])
        for j,m in enumerate(mis):
            print(f"  MIS[{j}] expect={m.get('expect')} pattern={m.get('pattern')} msg={m.get('message')}")
