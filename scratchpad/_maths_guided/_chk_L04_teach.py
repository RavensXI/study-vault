import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
teach=pd["guided"]["teach"]
for tier in ["bronze","silver","gold"]:
    t=teach.get(tier,{})
    print(f"\n############## teach.{tier} ##############")
    disp=t.get("display","")
    svgs=re.findall(r'<svg.*?</svg>',disp,flags=re.S)
    for s in svgs:
        # extract text labels
        labels=re.findall(r'>([^<]+)</text>',s)
        aria=re.search(r'aria-label="([^"]*)"',s)
        print("  SVG aria:",aria.group(1) if aria else None)
        print("  SVG labels:",labels)
    txt=re.sub(r'<svg.*?</svg>','[SVG]',disp,flags=re.S)
    print("  display:",txt)
    for i,st in enumerate(t.get("steps",[])):
        keys={k:st[k] for k in st if k in ("pre","post","answer","phase","say","done")}
        print(f"   step[{i}]:",json.dumps(keys,ensure_ascii=False))
