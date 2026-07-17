import json,re
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
teach=pd["guided"]["teach"]
for tier in ["bronze","silver","gold"]:
    t=teach.get(tier,{})
    print(f"\n===== TEACH {tier} =====")
    print("problem:",t.get("problem"))
    for i,s in enumerate(t.get("steps",[])):
        s2={k:(re.sub(r'<svg.*?</svg>','[SVG]',v,flags=re.S) if isinstance(v,str) else v) for k,v in s.items()}
        print(f" [{i}]",json.dumps(s2,ensure_ascii=False))
